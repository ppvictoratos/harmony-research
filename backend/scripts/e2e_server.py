"""Run the API against a throwaway end-to-end test database (never the real one).

Creates <your database>_e2e if missing, migrates it, wipes it, loads small fixtures,
then serves the API. Playwright starts this automatically (see web/playwright.config.ts).

Usage (from backend/):
    PYTHONPATH=. ./venv/bin/python scripts/e2e_server.py --port 8001
"""
import argparse
import os
from datetime import datetime

import app.config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def e2e_url() -> str:
    url = make_url(app.config.settings.database_url)
    name = url.database or "harmony_db"
    return url.set(database=name if name.endswith("_e2e") else f"{name}_e2e").render_as_string(hide_password=False)


FIXTURES = [
    {"study_id": "pubmed_e2e1", "title": "Rhythmic auditory cueing improves gait speed in Parkinson's disease",
     "authors": "Rivera A., Chen L.", "year": 2024, "source": "pubmed",
     "abstract": "Metronome cues at 110% of baseline cadence improved gait speed.",
     "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
    {"study_id": "pubmed_e2e2", "title": "Group singing and speech loudness in Parkinson's disease",
     "authors": "Okafor N.", "year": 2021, "source": "pubmed",
     "abstract": "Weekly choir sessions increased vocal loudness."},
    {"study_id": "pubmed_e2e3", "title": "Dance therapy and balance: a randomized trial",
     "authors": "Larsen M.", "year": 2019, "source": "pubmed", "abstract": "Tango classes twice weekly."},
    {"study_id": "clinicaltrials_NCTE2E1", "title": "Music therapy for freezing of gait",
     "authors": "Test University Hospital", "year": 2025, "source": "clinicaltrials",
     "intervention_type": "behavioral", "outcomes": "Freezing of Gait Questionnaire|Gait speed",
     "sample_size": 48, "abstract": "Participants walk to music matched to their cadence.",
     "url": "https://clinicaltrials.gov/study/NCTE2E1"},
    {"study_id": "europepmc_PPR_E2E1", "title": "Walking to the beat with drumming: a preprint",
     "authors": "Ito K.", "year": 2026, "source": "preprint", "abstract": "Drum patterns paced walking.",
     "url": "https://europepmc.org/article/PPR/E2E1"},
]


def prepare_database(url: str) -> None:
    target = make_url(url)
    admin = create_engine(target.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": target.database}).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{target.database}"'))
    admin.dispose()

    from alembic import command
    from alembic.config import Config

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    command.upgrade(Config(os.path.join(here, "alembic.ini")), "head")

    from app.database import SessionLocal
    from app.models import Evidence

    db = SessionLocal()
    try:
        db.execute(text("TRUNCATE study_sessions, studies, evidence RESTART IDENTITY CASCADE"))
        now = datetime(2026, 1, 1)
        db.add_all(Evidence(**f, date_added=now, created_at=now) for f in FIXTURES)
        db.commit()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--web-origin", default="http://localhost:3100")
    args = parser.parse_args()

    url = e2e_url()
    assert make_url(url).database.endswith("_e2e"), "refusing to run e2e against a non-e2e database"
    # Point every later import (database engine, Alembic env, CORS) at the e2e settings
    os.environ["DATABASE_URL"] = url
    os.environ["CORS_ORIGINS"] = f'["{args.web_origin}"]'
    app.config.settings = app.config.Settings()

    prepare_database(url)
    print(f"e2e database ready: {make_url(url).database}", flush=True)

    import uvicorn

    from app.main import app as api

    uvicorn.run(api, host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
