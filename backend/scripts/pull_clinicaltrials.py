"""Pull music + Parkinson's trials from ClinicalTrials.gov into the evidence table.

Usage (from backend/):
    PYTHONPATH=. ./venv/bin/python scripts/pull_clinicaltrials.py [--query QUERY] [--max N]
"""
import argparse
import logging

from app.database import SessionLocal
from app.integrations.clinicaltrials import ClinicalTrialsClient
from app.models import Evidence
from app.services import ingest_evidence

DEFAULT_CONDITION = "Parkinson"
DEFAULT_QUERY = (
    'music OR musical OR singing OR metronome OR "rhythmic auditory" '
    'OR "auditory cueing" OR "auditory cues" OR "auditory cue"'
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--condition", default=DEFAULT_CONDITION)
    parser.add_argument("--max", type=int, default=1000)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    studies = ClinicalTrialsClient().search(args.query, max_results=args.max, condition=args.condition)
    print(f"Fetched {len(studies)} trials from ClinicalTrials.gov")

    db = SessionLocal()
    try:
        inserted = ingest_evidence(studies, db)
        total = db.query(Evidence).filter(Evidence.source == "clinicaltrials").count()
    finally:
        db.close()
    print(f"Inserted {inserted} new, {total} ClinicalTrials.gov trials in database")


if __name__ == "__main__":
    main()
