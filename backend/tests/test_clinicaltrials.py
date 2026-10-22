from unittest.mock import MagicMock, patch

import pytest
import requests

from app.integrations.clinicaltrials import ClinicalTrialsClient


def _study(nct_id, **overrides):
    proto = {
        "identificationModule": {
            "nctId": nct_id,
            "briefTitle": "Music Therapy for Parkinson's",
            "officialTitle": "Music Therapy for Parkinson's Disease: A Randomized Trial",
            "organization": {"fullName": "Test Hospital"},
        },
        "statusModule": {"startDateStruct": {"date": "2020-03"}},
        "descriptionModule": {"briefSummary": "Rhythmic auditory cueing for gait."},
        "designModule": {"enrollmentInfo": {"count": 40}},
        "armsInterventionsModule": {"interventions": [{"type": "BEHAVIORAL"}, {"type": "OTHER"}, {"type": "BEHAVIORAL"}]},
        "outcomesModule": {"primaryOutcomes": [{"measure": "Gait Speed"}, {"measure": "UPDRS III"}]},
    }
    proto.update(overrides)
    return {"protocolSection": proto}


def _resp(json_data=None, status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(str(status))
    else:
        resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def client():
    c = ClinicalTrialsClient()
    c.min_interval = 0
    return c


def test_search_returns_parsed_studies(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value = _resp({"studies": [_study("NCT12345678")]})
        result = client.search("music therapy", condition="Parkinson")

    assert result == [{
        "study_id": "clinicaltrials_NCT12345678",
        "title": "Music Therapy for Parkinson's Disease: A Randomized Trial",
        "authors": "Test Hospital",
        "year": 2020,
        "abstract": "Rhythmic auditory cueing for gait.",
        "intervention_type": "behavioral|other",
        "outcomes": "Gait Speed|UPDRS III",
        "sample_size": 40,
        "source": "clinicaltrials",
        "url": "https://clinicaltrials.gov/study/NCT12345678",
    }]
    params = mock_get.call_args.kwargs["params"]
    assert params["query.cond"] == "Parkinson"


def test_year_falls_back_to_submit_date(client):
    study = _study("NCT1", statusModule={"studyFirstSubmitDate": "2018-07-02"})
    assert client._parse_study(study)["year"] == 2018


def test_search_handles_empty_results(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value = _resp({"studies": []})
        assert client.search("nonexistent") == []


def test_search_follows_pagination(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            _resp({"studies": [_study("NCT1")], "nextPageToken": "abc"}),
            _resp({"studies": [_study("NCT2")]}),
        ]
        result = client.search("music")
    assert [s["study_id"] for s in result] == ["clinicaltrials_NCT1", "clinicaltrials_NCT2"]
    assert mock_get.call_args_list[1].kwargs["params"]["pageToken"] == "abc"


def test_search_keeps_pages_fetched_before_error(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            _resp({"studies": [_study("NCT1")], "nextPageToken": "abc"}),
            requests.ConnectionError("Network error"),
        ]
        result = client.search("music")
    assert [s["study_id"] for s in result] == ["clinicaltrials_NCT1"]


def test_retries_on_rate_limit(client):
    with patch("requests.get") as mock_get, patch("time.sleep"):
        mock_get.side_effect = [_resp(status=429), _resp({"studies": []})]
        assert client.search("q") == []
    assert mock_get.call_count == 2
