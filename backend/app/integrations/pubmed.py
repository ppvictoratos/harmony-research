import logging
import re
import time
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET

import requests

logger = logging.getLogger(__name__)


class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    TOOL = "harmony-research"
    FETCH_BATCH = 200  # efetch IDs per request
    MAX_RETRIES = 3

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # NCBI allows 3 req/sec without a key, 10 with one
        self.min_interval = 0.1 if api_key else 0.34
        self.last_request_time = 0.0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def _get(self, endpoint: str, params: Dict) -> requests.Response:
        """GET with rate limiting and exponential backoff on 429/5xx."""
        params = {**params, "tool": self.TOOL}
        if self.api_key:
            params["api_key"] = self.api_key
        for attempt in range(self.MAX_RETRIES + 1):
            self._rate_limit()
            resp = requests.get(f"{self.BASE_URL}/{endpoint}", params=params, timeout=30)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.MAX_RETRIES:
                wait = 2 ** attempt
                logger.warning(f"PubMed {endpoint} returned {resp.status_code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        raise RuntimeError("unreachable")

    def search(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search PubMed for query, return list of studies"""
        try:
            resp = self._get("esearch.fcgi", {
                "db": "pubmed",
                "term": query,
                "retmax": min(max_results, 10000),
                "retmode": "json",
                "sort": "relevance",
            })
            pmids = resp.json().get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            logger.error(f"PubMed search error: {e}")
            return []

        if not pmids:
            logger.info(f"No results for query: {query}")
            return []

        studies = []
        for i in range(0, len(pmids[:max_results]), self.FETCH_BATCH):
            studies.extend(self._fetch_details(pmids[i:i + self.FETCH_BATCH]))
        return studies

    def _fetch_details(self, pmids: List[str]) -> List[Dict]:
        """Fetch full details for a list of PMIDs"""
        try:
            resp = self._get("efetch.fcgi", {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
            })
            root = ET.fromstring(resp.content)
        except Exception as e:
            logger.error(f"PubMed fetch error for {len(pmids)} PMIDs: {e}")
            return []

        studies = []
        for article in root.findall(".//PubmedArticle"):
            study = self._parse_article(article)
            if study:
                studies.append(study)
        return studies

    @staticmethod
    def _text(elem: Optional[ET.Element]) -> str:
        """Full text of an element, including inline markup like <i>."""
        if elem is None:
            return ""
        return " ".join("".join(elem.itertext()).split())

    @staticmethod
    def _parse_year(article: ET.Element) -> Optional[int]:
        year = article.findtext(".//Article/Journal/JournalIssue/PubDate/Year")
        if not year:
            # e.g. <MedlineDate>2019 Nov-Dec</MedlineDate>
            medline = article.findtext(".//Article/Journal/JournalIssue/PubDate/MedlineDate") or ""
            match = re.search(r"\b(19|20)\d{2}\b", medline)
            year = match.group(0) if match else None
        if not year:
            year = article.findtext(".//ArticleDate/Year")
        return int(year) if year else None

    def _parse_article(self, article: ET.Element) -> Optional[Dict]:
        """Extract structured data from a PubmedArticle XML element"""
        try:
            pmid = article.findtext("MedlineCitation/PMID")
            if not pmid:
                return None

            authors = []
            for author in article.findall(".//Article/AuthorList/Author"):
                last = author.findtext("LastName")
                if last:
                    first = author.findtext("ForeName") or author.findtext("Initials") or ""
                    authors.append(f"{last} {first[0]}." if first else last)
                elif author.findtext("CollectiveName"):
                    authors.append(author.findtext("CollectiveName"))

            # Structured abstracts have several labelled sections
            sections = []
            for part in article.findall(".//Abstract/AbstractText"):
                text = self._text(part)
                label = part.get("Label")
                if text:
                    sections.append(f"{label}: {text}" if label else text)

            return {
                "study_id": f"pubmed_{pmid}",
                "title": self._text(article.find(".//ArticleTitle"))[:500],
                "authors": ", ".join(authors[:5]),  # Limit to first 5
                "year": self._parse_year(article),
                "abstract": "\n".join(sections),
                "source": "pubmed",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            }
        except Exception as e:
            logger.warning(f"Failed to parse article: {e}")
            return None
