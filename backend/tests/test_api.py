import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base, Evidence


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    with TestSession() as db:
        db.add_all([
            Evidence(study_id="pubmed_1", title="Rhythmic auditory cueing and gait", authors="Smith J.",
                     year=2020, abstract="Metronome at 110% of cadence.", source="pubmed"),
            Evidence(study_id="pubmed_2", title="Singing for speech in Parkinson's", authors="Lee K.",
                     year=2018, source="pubmed"),
            Evidence(study_id="pubmed_3", title="Dance therapy", year=None, source="pubmed"),
            Evidence(study_id="clinicaltrials_NCT1", title="Music therapy trial", authors="Test Hospital",
                     year=2022, intervention_type="behavioral", outcomes="Gait Speed",
                     source="clinicaltrials"),
            Evidence(study_id="clinicaltrials_NCT2", title="Untyped trial", year=2022,
                     intervention_type="unknown", source="clinicaltrials"),
        ])
        db.commit()

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_is_paginated_newest_first(client):
    body = client.get("/api/evidence", params={"page": 1, "page_size": 2}).json()
    assert body["total"] == 5
    assert [r["study_id"] for r in body["results"]] == ["clinicaltrials_NCT2", "clinicaltrials_NCT1"]

    page2 = client.get("/api/evidence", params={"page": 2, "page_size": 2}).json()
    assert [r["study_id"] for r in page2["results"]] == ["pubmed_1", "pubmed_2"]
    page3 = client.get("/api/evidence", params={"page": 3, "page_size": 2}).json()
    # Missing years sort last
    assert [r["study_id"] for r in page3["results"]] == ["pubmed_3"]


def test_list_filters(client):
    body = client.get("/api/evidence", params={"source": "pubmed", "year_from": 2019}).json()
    assert [r["study_id"] for r in body["results"]] == ["pubmed_1"]


def test_search_matches_title_authors_abstract_outcomes(client):
    def ids(q):
        return {r["study_id"] for r in client.get("/api/evidence/search", params={"q": q}).json()["results"]}

    assert ids("GAIT") == {"pubmed_1", "clinicaltrials_NCT1"}  # title + outcomes, case-insensitive
    assert ids("lee") == {"pubmed_2"}
    assert ids("metronome") == {"pubmed_1"}


def test_search_treats_wildcards_literally(client):
    # Only the abstract containing a literal "%" matches, not every row
    assert client.get("/api/evidence/search", params={"q": "%"}).json()["total"] == 1
    assert client.get("/api/evidence/search", params={"q": "_"}).json()["total"] == 0
    assert client.get("/api/evidence/search", params={"q": "110%"}).json()["total"] == 1


def test_search_empty_results_and_validation(client):
    assert client.get("/api/evidence/search", params={"q": "zzz"}).json() == {
        "total": 0, "page": 1, "page_size": 20, "results": [],
    }
    assert client.get("/api/evidence/search", params={"q": ""}).status_code == 422
    assert client.get("/api/evidence", params={"page_size": 101}).status_code == 422


def test_stats(client):
    body = client.get("/api/evidence/stats").json()
    assert body == {
        "total_studies": 5,
        "by_source": {"pubmed": 3, "clinicaltrials": 2},
        "by_year": {"2018": 1, "2020": 1, "2022": 2, "unknown": 1},
        "by_intervention": {"behavioral": 1, "unknown": 4},
    }


def test_cors_allows_web_ui(client):
    resp = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert resp.headers["access-control-allow-origin"] == "http://localhost:3000"
