from unittest.mock import MagicMock, patch

import pytest
import requests

from app.integrations.europepmc import EuropePMCClient


def _resp(json_data=None, status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(str(status))
    else:
        resp.raise_for_status.return_value = None
    return resp


PREPRINT = {
    "id": "PPR1250561",
    "source": "PPR",
    "title": "Walking to the beat:  music and gait",
    "authorString": "Emerick M, Grahn JA.",
    "pubYear": "2026",
    "abstractText": "Walking impairments in Parkinson's disease.",
}
MEDLINE = {
    "id": "12345",
    "source": "MED",
    "pmid": "12345",
    "title": "Music therapy for Parkinson's",
    "authorString": "Smith J.",
    "pubYear": "2020",
}
THESIS = {"id": "ETH1", "source": "ETH", "title": "A thesis", "pubYear": ""}


@pytest.fixture
def client():
    c = EuropePMCClient()
    c.min_interval = 0
    return c


def _page(records, cursor):
    return _resp({"resultList": {"result": records}, "nextCursorMark": cursor})


def test_parses_sources_and_follows_cursor(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [_page([PREPRINT, MEDLINE], "c2"), _page([THESIS], "c3"), _page([], "c3")]
        result = client.search("music AND parkinson*")

    preprint, medline, thesis = result
    assert preprint == {
        "study_id": "europepmc_PPR_PPR1250561",
        "title": "Walking to the beat: music and gait",
        "authors": "Emerick M, Grahn JA",
        "year": 2026,
        "abstract": "Walking impairments in Parkinson's disease.",
        "source": "preprint",
        "url": "https://europepmc.org/article/PPR/PPR1250561",
    }
    # PubMed records reuse the PubMed identity so they dedupe against PubMedClient
    assert medline["study_id"] == "pubmed_12345"
    assert medline["source"] == "pubmed"
    assert thesis["source"] == "europepmc"
    assert thesis["year"] is None

    assert mock_get.call_args_list[0].kwargs["params"]["cursorMark"] == "*"
    assert mock_get.call_args_list[1].kwargs["params"]["cursorMark"] == "c2"


def test_stops_when_cursor_does_not_advance(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value = _page([PREPRINT], "*")
        assert len(client.search("q")) == 1
    assert mock_get.call_count == 1


def test_keeps_pages_fetched_before_error(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [_page([PREPRINT], "c2"), requests.ConnectionError("down")]
        assert [s["study_id"] for s in client.search("q")] == ["europepmc_PPR_PPR1250561"]


def test_retries_on_rate_limit(client):
    with patch("requests.get") as mock_get, patch("time.sleep"):
        mock_get.side_effect = [_resp(status=503), _page([], "*")]
        assert client.search("q") == []
    assert mock_get.call_count == 2
