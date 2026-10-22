import logging
import re
import time
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class ClinicalTrialsClient:
    BASE_URL = "https://clinicaltrials.gov/api/v2"
    PAGE_SIZE = 100
    MAX_RETRIES = 3

    def __init__(self):
        self.min_interval = 0.1
        self.last_request_time = 0.0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def _get(self, params: Dict) -> Dict:
        """GET /studies with rate limiting and exponential backoff on 429/5xx."""
        for attempt in range(self.MAX_RETRIES + 1):
            self._rate_limit()
            resp = requests.get(f"{self.BASE_URL}/studies", params=params, timeout=30)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.MAX_RETRIES:
                wait = 2 ** attempt
                logger.warning(f"ClinicalTrials returned {resp.status_code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError("unreachable")

    def search(self, query: str, max_results: int = 100, condition: Optional[str] = None) -> List[Dict]:
        """Search ClinicalTrials.gov for query, following pagination up to max_results"""
        params = {"query.term": query, "pageSize": min(max_results, self.PAGE_SIZE)}
        if condition:
            params["query.cond"] = condition

        studies: List[Dict] = []
        try:
            while len(studies) < max_results:
                data = self._get(params)
                for study in data.get("studies", []):
                    parsed = self._parse_study(study)
                    if parsed:
                        studies.append(parsed)
                token = data.get("nextPageToken")
                if not token:
                    break
                params["pageToken"] = token
        except Exception as e:
            # Keep whatever pages we already have
            logger.error(f"ClinicalTrials search error after {len(studies)} studies: {e}")
        return studies[:max_results]

    @staticmethod
    def _parse_year(date: Optional[str]) -> Optional[int]:
        match = re.match(r"(\d{4})", date or "")
        return int(match.group(1)) if match else None

    def _parse_study(self, study: Dict) -> Optional[Dict]:
        """Extract structured data from ClinicalTrials study JSON"""
        try:
            proto = study.get("protocolSection", {})
            ident = proto.get("identificationModule", {})
            status = proto.get("statusModule", {})
            design = proto.get("designModule", {})
            inter = proto.get("armsInterventionsModule", {})
            outcome = proto.get("outcomesModule", {})
            desc = proto.get("descriptionModule", {})

            nct_id = ident.get("nctId")
            if not nct_id:
                return None

            year = self._parse_year(status.get("startDateStruct", {}).get("date"))
            if year is None:
                year = self._parse_year(status.get("studyFirstSubmitDate"))

            intervention_types = sorted({
                iv.get("type", "").lower() for iv in inter.get("interventions", []) if iv.get("type")
            })
            outcomes_list = [
                o.get("measure", "") for o in outcome.get("primaryOutcomes", [])[:3] if o.get("measure")
            ]

            return {
                "study_id": f"clinicaltrials_{nct_id}",
                "title": (ident.get("officialTitle") or ident.get("briefTitle") or "")[:500],
                "authors": ident.get("organization", {}).get("fullName", ""),
                "year": year,
                "abstract": desc.get("briefSummary", ""),
                "intervention_type": "|".join(intervention_types)[:100] if intervention_types else "unknown",
                "outcomes": "|".join(outcomes_list),
                "sample_size": design.get("enrollmentInfo", {}).get("count"),
                "source": "clinicaltrials",
                "url": f"https://clinicaltrials.gov/study/{nct_id}",
            }
        except Exception as e:
            logger.warning(f"Failed to parse study: {e}")
            return None
