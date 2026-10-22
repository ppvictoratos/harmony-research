from unittest.mock import MagicMock, patch

import pytest
import requests

from app.integrations.pubmed import PubMedClient

ARTICLE_XML = b"""<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345</PMID>
      <Article>
        <Journal><JournalIssue><PubDate><Year>2020</Year></PubDate></JournalIssue></Journal>
        <ArticleTitle>Music Therapy for <i>Parkinson's</i> Disease</ArticleTitle>
        <Abstract>
          <AbstractText Label="BACKGROUND">Rhythmic cues at 120 BPM.</AbstractText>
          <AbstractText Label="RESULTS">Gait speed improved.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author><LastName>Smith</LastName><ForeName>John</ForeName></Author>
          <Author><CollectiveName>PD Music Group</CollectiveName></Author>
        </AuthorList>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>67890</PMID>
      <Article>
        <Journal><JournalIssue><PubDate><MedlineDate>2019 Nov-Dec</MedlineDate></PubDate></JournalIssue></Journal>
        <ArticleTitle>No abstract here</ArticleTitle>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>"""


def _resp(json_data=None, content=b"", status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    resp.content = content
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(str(status))
    else:
        resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def client():
    c = PubMedClient()
    c.min_interval = 0
    return c


def test_search_returns_parsed_studies(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            _resp({"esearchresult": {"idlist": ["12345", "67890"]}}),
            _resp(content=ARTICLE_XML),
        ]
        result = client.search("music therapy parkinson")

    assert len(result) == 2
    first, second = result
    assert first["study_id"] == "pubmed_12345"
    assert first["title"] == "Music Therapy for Parkinson's Disease"
    assert first["authors"] == "Smith J., PD Music Group"
    assert first["year"] == 2020
    assert first["abstract"] == "BACKGROUND: Rhythmic cues at 120 BPM.\nRESULTS: Gait speed improved."
    assert first["url"] == "https://pubmed.ncbi.nlm.nih.gov/12345/"
    assert second["year"] == 2019
    assert second["abstract"] == ""

    esearch_params = mock_get.call_args_list[0].kwargs["params"]
    assert esearch_params["retmode"] == "json"


def test_search_handles_empty_results(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value = _resp({"esearchresult": {"idlist": []}})
        assert client.search("nonexistent query") == []


def test_search_handles_network_error(client):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.ConnectionError("Network error")
        assert client.search("music therapy") == []


def test_fetch_is_batched(client):
    client.FETCH_BATCH = 1
    with patch("requests.get") as mock_get:
        mock_get.side_effect = [
            _resp({"esearchresult": {"idlist": ["1", "2"]}}),
            _resp(content=b"<PubmedArticleSet/>"),
            _resp(content=b"<PubmedArticleSet/>"),
        ]
        client.search("q")
    assert mock_get.call_count == 3


def test_retries_on_rate_limit(client):
    with patch("requests.get") as mock_get, patch("time.sleep"):
        mock_get.side_effect = [
            _resp(status=429),
            _resp({"esearchresult": {"idlist": []}}),
        ]
        assert client.search("q") == []
    assert mock_get.call_count == 2
