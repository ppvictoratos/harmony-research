"""Pull music + Parkinson's papers from PubMed into the evidence table.

Usage (from backend/):
    ./venv/bin/python scripts/pull_pubmed.py [--query QUERY] [--max N]
"""
import argparse
import logging
import os

from app.database import SessionLocal
from app.integrations.pubmed import PubMedClient
from app.models import Evidence
from app.services import ingest_evidence

DEFAULT_QUERY = (
    '(music[tiab] OR musical[tiab] OR "rhythmic auditory"[tiab] OR "auditory cueing"[tiab] '
    'OR "auditory cues"[tiab] OR singing[tiab] OR metronome[tiab] '
    'OR "music therapy"[mh] OR music[mh]) '
    'AND (parkinson*[tiab] OR "parkinson disease"[mh])'
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--max", type=int, default=1000)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = PubMedClient(api_key=os.getenv("PUBMED_API_KEY") or None)
    studies = client.search(args.query, max_results=args.max)
    print(f"Fetched {len(studies)} papers from PubMed")

    db = SessionLocal()
    try:
        inserted = ingest_evidence(studies, db)
        total = db.query(Evidence).filter(Evidence.source == "pubmed").count()
    finally:
        db.close()
    print(f"Inserted {inserted} new, {total} PubMed papers in database")


if __name__ == "__main__":
    main()
