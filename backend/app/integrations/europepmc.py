import logging
import time
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class EuropePMCClient:
    """Europe PMC REST search: PubMed records plus preprints, PMC-only papers and theses."""

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    PAGE_SIZE = 500
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
        """GET /search with rate limiting and exponential backoff on 429/5xx."""
        for attempt in range(self.MAX_RETRIES + 1):
            self._rate_limit()
            resp = requests.get(f"{self.BASE_URL}/search", params=params, timeout=30)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.MAX_RETRIES:
                wait = 2 ** attempt
                logger.warning(f"Europe PMC returned {resp.status_code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError("unreachable")

    def search(self, query: str, max_results: int = 1000) -> List[Dict]:
        """Search Europe PMC, following cursor pagination up to max_results"""
        params = {
            "query": query,
            "format": "json",
            "resultType": "core",  # includes abstracts
            "pageSize": min(max_results, self.PAGE_SIZE),
            "cursorMark": "*",
        }
        studies: List[Dict] = []
        try:
            while len(studies) < max_results:
                data = self._get(dict(params))
                results = data.get("resultList", {}).get("result", [])
                for record in results:
                    parsed = self._parse_record(record)
                    if parsed:
                        studies.append(parsed)
                next_cursor = data.get("nextCursorMark")
                if not results or not next_cursor or next_cursor == params["cursorMark"]:
                    break
                params["cursorMark"] = next_cursor
        except Exception as e:
            # Keep whatever pages we already have
            logger.error(f"Europe PMC search error after {len(studies)} records: {e}")
        return studies[:max_results]

    @staticmethod
    def _parse_record(record: Dict) -> Optional[Dict]:
        try:
            src = record.get("source")
            rec_id = record.get("id")
            if not src or not rec_id or not record.get("title"):
                return None

            year = record.get("pubYear")
            base = {
                "title": " ".join(record["title"].split())[:500],
                "authors": ", ".join(
                    a.strip() for a in (record.get("authorString") or "").rstrip(".").split(",")[:5] if a.strip()
                ),
                "year": int(year) if year and year.isdigit() else None,
                "abstract": record.get("abstractText") or "",
            }

            pmid = record.get("pmid")
            if pmid:
                # Same identity as PubMedClient so the paper is never stored twice
                return {
                    **base,
                    "study_id": f"pubmed_{pmid}",
                    "source": "pubmed",
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                }

            return {
                **base,
                "study_id": f"europepmc_{src}_{rec_id}"[:50],
                # Preprints are not peer reviewed, so keep them clearly separate
                "source": "preprint" if src == "PPR" else "europepmc",
                "url": f"https://europepmc.org/article/{src}/{rec_id}",
            }
        except Exception as e:
            logger.warning(f"Failed to parse Europe PMC record: {e}")
            return None
