"""Pull music + Parkinson's records from Europe PMC (adds preprints, PMC-only papers, theses).

Usage (from backend/):
    PYTHONPATH=. ./venv/bin/python scripts/pull_europepmc.py [--query QUERY] [--max N]
"""
import argparse
import logging

from sqlalchemy import func

from app.database import SessionLocal
from app.integrations.europepmc import EuropePMCClient
from app.models import Evidence
from app.services import ingest_evidence

MUSIC_TERMS = (
    '(music OR musical OR singing OR metronome OR "rhythmic auditory" '
    'OR "auditory cueing" OR "auditory cues" OR "auditory cue")'
)
DEFAULT_QUERY = f"TITLE_ABS:{MUSIC_TERMS} AND TITLE_ABS:parkinson*"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--max", type=int, default=2000)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    studies = EuropePMCClient().search(args.query, max_results=args.max)
    print(f"Fetched {len(studies)} records from Europe PMC")

    db = SessionLocal()
    try:
        inserted = ingest_evidence(studies, db)
        by_source = dict(db.query(Evidence.source, func.count(Evidence.id)).group_by(Evidence.source).all())
    finally:
        db.close()
    print(f"Inserted {inserted} new records. Database now: {by_source}")


if __name__ == "__main__":
    main()
