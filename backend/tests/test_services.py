import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Evidence
from app.services import ingest_evidence


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False)()
    yield session
    session.close()


def test_skips_duplicates_within_batch(db):
    studies = [
        {"study_id": "test_1", "title": "Music therapy study", "source": "pubmed"},
        {"study_id": "test_1", "title": "Music therapy study", "source": "pubmed"},
    ]
    assert ingest_evidence(studies, db) == 1
    assert db.query(Evidence).count() == 1


def test_skips_existing_rows_on_rerun(db):
    studies = [{"study_id": "test_1", "title": "Music therapy study", "source": "pubmed", "abstract": "a"}]
    assert ingest_evidence(studies, db) == 1
    assert ingest_evidence(studies, db) == 0
    assert db.query(Evidence).one().abstract == "a"


def test_skips_rows_without_title(db):
    assert ingest_evidence([{"study_id": "x", "title": "", "source": "pubmed"}], db) == 0


def test_skips_off_topic_records(db):
    studies = [
        {"study_id": "a", "title": "Rhythmic auditory cueing for gait", "source": "pubmed"},
        {"study_id": "b", "title": "Deep brain stimulation RNA protocol",
         "abstract": "Patients listened to music.", "source": "preprint"},
        {"study_id": "c", "title": "Gait training outcomes",
         "abstract": "Metronome-paced walking and music.", "source": "pubmed"},
    ]
    assert ingest_evidence(studies, db) == 2
    assert {e.study_id for e in db.query(Evidence)} == {"a", "c"}
