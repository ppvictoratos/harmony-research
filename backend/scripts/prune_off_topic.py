"""Remove evidence records that aren't about music, rhythm or sound (see app/relevance.py).

Usage (from backend/):
    PYTHONPATH=. ./venv/bin/python scripts/prune_off_topic.py           # dry run: list what would go
    PYTHONPATH=. ./venv/bin/python scripts/prune_off_topic.py --apply   # delete them

Ingestion applies the same rule, so deleted records only come back if the rule is
loosened and the pull scripts are run again.
"""
import argparse

from app.database import SessionLocal
from app.models import Evidence
from app.relevance import is_music_relevant


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="actually delete the records")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        off_topic = [
            e for e in db.query(Evidence).all()
            if not is_music_relevant({"title": e.title, "abstract": e.abstract, "outcomes": e.outcomes})
        ]
        for e in off_topic:
            print(f"  {e.source:<14} {e.year or '':<5} {e.title[:90]}")
        if args.apply:
            for e in off_topic:
                db.delete(e)
            db.commit()
            print(f"Deleted {len(off_topic)} off-topic records; {db.query(Evidence).count()} remain")
        else:
            print(f"{len(off_topic)} off-topic records would be deleted. Re-run with --apply.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
