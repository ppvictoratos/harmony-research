import random
from collections import Counter
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base
from app.study_design import block_randomized_schedule


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    event.listen(engine, "connect", lambda conn, _: conn.execute("PRAGMA foreign_keys=ON"))
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _create(client, **overrides):
    body = {
        "title": "Guitar vs Endel",
        "question": "Which lifts my mood more?",
        "conditions": ["Guitar", "Endel", "Silence"],
        "session_minutes": 20,
        "sessions_per_condition": 4,
        "start_date": "2026-11-01",
        **overrides,
    }
    return client.post("/api/studies", json=body)


def test_schedule_is_balanced_in_every_block():
    schedule = block_randomized_schedule(["A", "B", "C"], 5, date(2026, 1, 1), random.Random(1))
    assert len(schedule) == 15
    for i in range(0, 15, 3):
        assert sorted(s["condition"] for s in schedule[i:i + 3]) == ["A", "B", "C"]
    assert [s["planned_date"] for s in schedule] == [date(2026, 1, 1) + timedelta(days=i) for i in range(15)]
    assert [s["session_number"] for s in schedule] == list(range(1, 16))


def test_create_study_builds_schedule(client):
    resp = _create(client)
    assert resp.status_code == 201
    study = resp.json()
    assert study["total_sessions"] == 12
    assert study["completed_sessions"] == 0
    assert Counter(s["condition"] for s in study["sessions"]) == {"Guitar": 4, "Endel": 4, "Silence": 4}
    assert study["sessions"][0]["planned_date"] == "2026-11-01"
    assert client.get("/api/studies").json()[0]["title"] == "Guitar vs Endel"


@pytest.mark.parametrize("conditions", [["Only one"], ["A", "a"], ["A", " "], ["A", "B", "C", "D", "E", "F", "G"]])
def test_rejects_bad_conditions(client, conditions):
    assert _create(client, conditions=conditions).status_code == 422


def test_log_session_and_results(client):
    study = _create(client).json()
    sid = study["id"]
    by_condition = {}
    for s in study["sessions"]:
        by_condition.setdefault(s["condition"], []).append(s["id"])

    def log(session_id, before, after, **extra):
        return client.patch(f"/api/studies/{sid}/sessions/{session_id}",
                            json={"mood_before": before, "mood_after": after, "completed": True, **extra})

    assert log(by_condition["Guitar"][0], 4, 7, focus_before=3, focus_after=6).status_code == 200
    assert log(by_condition["Guitar"][1], 5, 6).status_code == 200
    assert log(by_condition["Silence"][0], 5, 5).status_code == 200

    results = client.get(f"/api/studies/{sid}/results").json()
    assert results["completed_sessions"] == 3
    guitar = next(c for c in results["conditions"] if c["condition"] == "Guitar")
    assert guitar["completed"] == 2
    assert guitar["mood_changes"] == [3, 1]
    assert guitar["mood_change_avg"] == 2.0
    assert guitar["focus_change_avg"] == 3.0
    endel = next(c for c in results["conditions"] if c["condition"] == "Endel")
    assert endel["completed"] == 0 and endel["mood_change_avg"] is None


def test_cannot_complete_without_mood_ratings(client):
    study = _create(client).json()
    session_id = study["sessions"][0]["id"]
    resp = client.patch(f"/api/studies/{study['id']}/sessions/{session_id}",
                        json={"mood_before": 5, "completed": True})
    assert resp.status_code == 422


def test_rating_bounds_and_uncomplete(client):
    study = _create(client).json()
    url = f"/api/studies/{study['id']}/sessions/{study['sessions'][0]['id']}"
    assert client.patch(url, json={"mood_before": 11}).status_code == 422
    assert client.patch(url, json={"mood_before": 0}).status_code == 422
    assert client.patch(url, json={"mood_before": 6, "mood_after": 8, "completed": True}).json()["completed_at"]
    undone = client.patch(url, json={"completed": False}).json()
    assert undone["completed_at"] is None
    assert undone["mood_before"] == 6  # ratings kept


def test_session_must_belong_to_study(client):
    first = _create(client).json()
    second = _create(client, title="Other").json()
    url = f"/api/studies/{second['id']}/sessions/{first['sessions'][0]['id']}"
    assert client.patch(url, json={"mood_before": 5}).status_code == 404


def test_delete_study(client):
    sid = _create(client).json()["id"]
    assert client.delete(f"/api/studies/{sid}").status_code == 204
    assert client.get(f"/api/studies/{sid}").status_code == 404
    assert client.get("/api/studies").json() == []
