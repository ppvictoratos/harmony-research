# Music Therapy Research Platform — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an evidence aggregator that pulls public music therapy + Parkinson's research, structures it, and exposes it via a web UI for browsing and filtering.

**Architecture:** Python backend (PostgreSQL + PubMed/ClinicalTrials.gov APIs) → TypeScript/React web UI. Scientific-agent-skills integration for future NLP/analysis layers. Start solo, publish v0.1 to GitHub by month 4.

**Tech Stack:** 
- Frontend: TypeScript, React, Vite
- Backend: Python 3.11+, FastAPI, SQLAlchemy
- Database: PostgreSQL 14+
- APIs: PubMed E-utilities, ClinicalTrials.gov API
- Testing: pytest (backend), vitest (frontend)
- Deployment: GitHub (code), local dev first

**Spec:** `/Users/panagiotis/Desktop/music-therapy-research-design.md` (Phase 1: Evidence Aggregator MVP, months 1–4)

## Global Constraints

- Public data only (PubMed, ClinicalTrials.gov, no patient data)
- Evidence schema: study_id, title, authors, year, intervention (music properties), outcomes, sample_size, effect_size, source, date_added
- No IRB/ethics approval needed (synthesis only, no primary data)
- Incremental GitHub release: v0.1 at month 4
- Python 3.11+ baseline (scientific-agent-skills compatibility)
- React 18+ for web UI

## Review Focus

1. **API rate-limiting:** PubMed and ClinicalTrials.gov have rate limits; scraper must handle backoff and errors gracefully without losing state
2. **Duplicate detection:** Same study may appear in PubMed and ClinicalTrials.gov; must avoid duplicates in evidence base
3. **Structured extraction:** Literature ingestion must reliably extract music intervention type (tempo, chord, rhythm) and outcome type (gait, motor, mood) from unstructured abstracts — test on real papers
4. **Search/filter correctness:** Web UI filter results must match database queries exactly; test edge cases (empty results, special chars, boolean filters)
5. **Data persistence:** PostgreSQL migrations must be reversible and idempotent; test rollback scenarios

---

## File Structure

```
harmony-research/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py (FastAPI app)
│   │   ├── models.py (SQLAlchemy ORM)
│   │   ├── schemas.py (Pydantic request/response)
│   │   ├── database.py (DB connection, session)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py (GET /evidence, /search, /stats)
│   │   └── integrations/
│   │       ├── __init__.py
│   │       ├── pubmed.py (PubMed API client)
│   │       └── clinicaltrials.py (ClinicalTrials.gov API client)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_api.py
│   │   ├── test_pubmed.py
│   │   └── test_clinicaltrials.py
│   ├── migrations/
│   │   ├── env.py (Alembic config)
│   │   ├── script.py.mako
│   │   └── versions/ (migration files)
│   ├── .env.example
│   ├── pyproject.toml
│   └── README.md
├── web/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles/
│   │   │   └── App.css
│   │   ├── components/
│   │   │   ├── EvidenceTable.tsx
│   │   │   ├── SearchForm.tsx
│   │   │   └── FilterPanel.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── Evidence.ts
│   ├── tests/
│   │   ├── EvidenceTable.test.tsx
│   │   └── SearchForm.test.tsx
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── README.md
├── .gitignore
├── .env.example
├── README.md
└── LICENSE (MIT)
```

---

## Tasks

### Task 1: Initialize GitHub Repository & Project Structure

**Files:**
- Create: `README.md` (project overview)
- Create: `LICENSE` (MIT)
- Create: `.gitignore`
- Create: `.env.example`
- Create: `backend/pyproject.toml`
- Create: `web/package.json`

**Interfaces:**
- Produces: GitHub repo ready for commits, local dev setup instructions

- [ ] **Step 1: Create GitHub repo locally**

```bash
cd /Users/panagiotis/Desktop
git init harmony-research
cd harmony-research
```

- [ ] **Step 2: Write README.md**

```markdown
# Harmony Research: Music Therapy + Parkinson's Evidence Platform

A research tool to discover musical elements that improve Parkinson's outcomes through evidence aggregation, gap analysis, and experiment design.

## Phase 1: Evidence Aggregator (Months 1–4)

- Pulls public research from PubMed, ClinicalTrials.gov
- Structures findings into searchable evidence base
- Web UI for browsing and filtering

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

### Web

```bash
cd web
npm install
npm run dev
```

## License

MIT
```

- [ ] **Step 3: Write LICENSE (MIT)**

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

- [ ] **Step 4: Write .gitignore**

```
# Backend
backend/venv/
backend/.env
backend/.env.local
backend/__pycache__/
backend/*.pyc
backend/.pytest_cache/
backend/.venv/
backend/db.sqlite3
backend/instance/

# Web
web/node_modules/
web/dist/
web/.env.local
web/.DS_Store

# General
.DS_Store
*.swp
*.swo
*.vscode/
.idea/
```

- [ ] **Step 5: Write .env.example**

```
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/harmony_db
PUBMED_API_KEY=your_pubmed_api_key_optional
LOG_LEVEL=INFO

# Web
VITE_API_BASE_URL=http://localhost:8000
```

- [ ] **Step 6: Write backend/pyproject.toml**

```toml
[project]
name = "harmony-research-backend"
version = "0.1.0"
description = "Evidence aggregator for music therapy + Parkinson's research"
requires-python = ">=3.11"
dependencies = [
    "fastapi==0.104.1",
    "sqlalchemy==2.0.23",
    "psycopg2-binary==2.9.9",
    "alembic==1.13.1",
    "requests==2.31.0",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
    "python-dotenv==1.0.0",
    "uvicorn==0.24.0",
    "pytest==7.4.3",
    "pytest-asyncio==0.21.1",
    "httpx==0.25.2",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

- [ ] **Step 7: Write web/package.json**

```json
{
  "name": "harmony-research-web",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.8",
    "vitest": "^1.0.4",
    "@testing-library/react": "^14.1.2"
  }
}
```

- [ ] **Step 8: Commit**

```bash
git add README.md LICENSE .gitignore .env.example backend/pyproject.toml web/package.json
git commit -m "init: scaffold harmony research project structure"
```

---

### Task 2: Set Up Database Schema & Migrations

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models.py`
- Create: `backend/migrations/env.py`
- Create: `backend/migrations/script.py.mako`
- Create: `backend/migrations/versions/001_create_evidence_table.py`

**Interfaces:**
- Produces: PostgreSQL Evidence table (study_id, title, authors, year, intervention_type, intervention_details, outcomes, sample_size, effect_size, source, url, date_added, created_at)

- [ ] **Step 1: Write backend/app/database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 2: Write backend/app/config.py (new file)**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/harmony_db"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 3: Write backend/app/models.py**

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(Integer, primary_key=True)
    study_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(500), nullable=False)
    authors = Column(Text)
    year = Column(Integer)
    intervention_type = Column(String(100))  # e.g., "music_alone", "music_pt", "music_ot"
    intervention_details = Column(Text)  # JSON string: {"tempo": 120, "key": "major", "rhythm": "4/4"}
    outcomes = Column(Text)  # JSON: {"outcome_type": "gait", "measure": "cadence", "effect_size": 0.5}
    sample_size = Column(Integer)
    effect_size = Column(Float)
    source = Column(String(50), nullable=False)  # "pubmed", "clinicaltrials"
    url = Column(String(500))
    date_added = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_evidence_source_year", "source", "year"),
        Index("ix_evidence_intervention", "intervention_type"),
    )
```

- [ ] **Step 4: Initialize Alembic**

```bash
cd backend
alembic init -t async migrations
```

- [ ] **Step 5: Write backend/migrations/env.py**

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.models import Base
from app.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 6: Create migration file backend/migrations/versions/001_create_evidence_table.py**

```python
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('study_id', sa.String(50), nullable=False, unique=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('authors', sa.Text(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('intervention_type', sa.String(100), nullable=True),
        sa.Column('intervention_details', sa.Text(), nullable=True),
        sa.Column('outcomes', sa.Text(), nullable=True),
        sa.Column('sample_size', sa.Integer(), nullable=True),
        sa.Column('effect_size', sa.Float(), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('url', sa.String(500), nullable=True),
        sa.Column('date_added', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_evidence_source_year', 'evidence', ['source', 'year'])
    op.create_index('ix_evidence_intervention', 'evidence', ['intervention_type'])

def downgrade() -> None:
    op.drop_table('evidence')
```

- [ ] **Step 7: Commit**

```bash
git add backend/app/database.py backend/app/config.py backend/app/models.py backend/migrations/
git commit -m "feat: create evidence database schema and alembic migrations"
```

---

### Task 3: Build PubMed API Integration

**Files:**
- Create: `backend/app/integrations/pubmed.py`
- Create: `backend/tests/test_pubmed.py`

**Interfaces:**
- Consumes: Nothing (external API only)
- Produces: `PubMedClient.search(query: str, max_results: int) -> List[dict]` returning `{study_id, title, authors, year, abstract}`

- [ ] **Step 1: Write backend/app/integrations/pubmed.py**

```python
import requests
from typing import List, Dict
import time
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.request_count = 0
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce 3 requests/sec for PubMed E-utilities"""
        elapsed = time.time() - self.last_request_time
        if elapsed < 0.33:
            time.sleep(0.33 - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search PubMed for query, return list of studies"""
        self._rate_limit()
        
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": min(max_results, 10000),
            "rettype": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            resp = requests.get(f"{self.BASE_URL}/esearch.fcgi", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])
            
            if not pmids:
                logger.info(f"No results for query: {query}")
                return []
            
            return self._fetch_details(pmids[:max_results])
        except Exception as e:
            logger.error(f"PubMed search error: {e}")
            return []
    
    def _fetch_details(self, pmids: List[str]) -> List[Dict]:
        """Fetch full details for a list of PMIDs"""
        self._rate_limit()
        
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "xml",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            resp = requests.get(f"{self.BASE_URL}/efetch.fcgi", params=params, timeout=10)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            
            studies = []
            for article in root.findall(".//PubmedArticle"):
                study = self._parse_article(article)
                if study:
                    studies.append(study)
            return studies
        except Exception as e:
            logger.error(f"PubMed fetch error: {e}")
            return []
    
    def _parse_article(self, article: ET.Element) -> Dict:
        """Extract structured data from a PubmedArticle XML element"""
        try:
            pmid_elem = article.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else None
            
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else ""
            
            year_elem = article.find(".//PubDate/Year")
            year = int(year_elem.text) if year_elem is not None else None
            
            authors = []
            for author in article.findall(".//Author"):
                last = author.find("LastName")
                first = author.find("ForeName")
                if last is not None:
                    name = last.text
                    if first is not None:
                        name += f" {first.text[0]}."
                    authors.append(name)
            
            abstract_elem = article.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else ""
            
            return {
                "study_id": f"pubmed_{pmid}",
                "title": title,
                "authors": ", ".join(authors[:5]),  # Limit to first 5
                "year": year,
                "abstract": abstract,
                "source": "pubmed",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            }
        except Exception as e:
            logger.warning(f"Failed to parse article: {e}")
            return None
```

- [ ] **Step 2: Write backend/tests/test_pubmed.py**

```python
import pytest
from app.integrations.pubmed import PubMedClient
from unittest.mock import patch, MagicMock
import json

@pytest.fixture
def client():
    return PubMedClient()

def test_search_returns_list(client):
    """Test that search returns a list"""
    with patch("requests.get") as mock_get:
        # Mock esearch response
        search_resp = MagicMock()
        search_resp.json.return_value = {
            "esearchresult": {
                "idlist": ["12345"],
                "count": "1"
            }
        }
        search_resp.raise_for_status.return_value = None
        
        # Mock efetch response
        fetch_resp = MagicMock()
        fetch_resp.content = b"""<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345</PMID>
      <Article>
        <ArticleTitle>Music Therapy for Parkinson's Disease</ArticleTitle>
        <AuthorList>
          <Author>
            <LastName>Smith</LastName>
            <ForeName>John</ForeName>
          </Author>
        </AuthorList>
        <PubDate>
          <Year>2020</Year>
        </PubDate>
        <Abstract>
          <AbstractText>This is a test abstract about music therapy.</AbstractText>
        </Abstract>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>"""
        fetch_resp.raise_for_status.return_value = None
        
        mock_get.side_effect = [search_resp, fetch_resp]
        
        result = client.search("music therapy parkinson")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["study_id"] == "pubmed_12345"
        assert "Music Therapy" in result[0]["title"]

def test_search_handles_empty_results(client):
    """Test that search handles empty results gracefully"""
    with patch("requests.get") as mock_get:
        resp = MagicMock()
        resp.json.return_value = {"esearchresult": {"idlist": []}}
        resp.raise_for_status.return_value = None
        mock_get.return_value = resp
        
        result = client.search("nonexistent query")
        assert result == []

def test_search_handles_network_error(client):
    """Test that search handles network errors gracefully"""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        result = client.search("music therapy")
        assert result == []
```

- [ ] **Step 3: Run tests**

```bash
cd backend
python -m pytest tests/test_pubmed.py -v
```

Expected: PASS (2 tests pass, 1 passes)

- [ ] **Step 4: Commit**

```bash
git add backend/app/integrations/pubmed.py backend/tests/test_pubmed.py
git commit -m "feat: implement PubMed API client with search and fetch"
```

---

### Task 4: Build ClinicalTrials.gov API Integration

**Files:**
- Create: `backend/app/integrations/clinicaltrials.py`
- Create: `backend/tests/test_clinicaltrials.py`

**Interfaces:**
- Consumes: Nothing (external API only)
- Produces: `ClinicalTrialsClient.search(query: str, max_results: int) -> List[dict]` returning `{study_id, title, year, intervention_type, outcomes}`

- [ ] **Step 1: Write backend/app/integrations/clinicaltrials.py**

```python
import requests
from typing import List, Dict
import time
import logging

logger = logging.getLogger(__name__)

class ClinicalTrialsClient:
    BASE_URL = "https://clinicaltrials.gov/api/v2"
    
    def __init__(self):
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Enforce rate limit for ClinicalTrials API"""
        elapsed = time.time() - self.last_request_time
        if elapsed < 0.1:
            time.sleep(0.1 - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search ClinicalTrials.gov for query"""
        self._rate_limit()
        
        params = {
            "query.term": query,
            "pageSize": min(max_results, 1000),
            "format": "json",
        }
        
        try:
            resp = requests.get(f"{self.BASE_URL}/studies", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            studies = []
            for study in data.get("studies", [])[:max_results]:
                parsed = self._parse_study(study)
                if parsed:
                    studies.append(parsed)
            return studies
        except Exception as e:
            logger.error(f"ClinicalTrials search error: {e}")
            return []
    
    def _parse_study(self, study: Dict) -> Dict:
        """Extract structured data from ClinicalTrials study JSON"""
        try:
            proto = study.get("protocolSection", {})
            ident = proto.get("identificationModule", {})
            design = proto.get("designModule", {})
            cond = proto.get("conditionsModule", {})
            inter = proto.get("armsInterventionsModule", {})
            outcome = proto.get("outcomesModule", {})
            
            nct_id = ident.get("nctId", "")
            title = ident.get("officialTitle", ident.get("briefTitle", ""))
            org = ident.get("organization", {}).get("name", "")
            
            start_date = ident.get("startDateStruct", {})
            year = int(start_date.get("year", 0)) if start_date.get("year") else None
            
            interventions = inter.get("interventions", [])
            intervention_types = []
            for iv in interventions:
                intervention_types.append(iv.get("type", ""))
            
            outcomes_list = []
            for out in outcome.get("primaryOutcomes", [])[:3]:
                outcomes_list.append(out.get("measure", ""))
            
            return {
                "study_id": f"clinicaltrials_{nct_id}",
                "title": title,
                "authors": org,
                "year": year,
                "intervention_type": "|".join(set(intervention_types)) if intervention_types else "unknown",
                "outcomes": "|".join(outcomes_list) if outcomes_list else "",
                "source": "clinicaltrials",
                "url": f"https://clinicaltrials.gov/study/{nct_id}"
            }
        except Exception as e:
            logger.warning(f"Failed to parse study: {e}")
            return None
```

- [ ] **Step 2: Write backend/tests/test_clinicaltrials.py**

```python
import pytest
from app.integrations.clinicaltrials import ClinicalTrialsClient
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    return ClinicalTrialsClient()

def test_search_returns_list(client):
    """Test that search returns a list"""
    with patch("requests.get") as mock_get:
        resp = MagicMock()
        resp.json.return_value = {
            "studies": [
                {
                    "protocolSection": {
                        "identificationModule": {
                            "nctId": "NCT12345678",
                            "officialTitle": "Music Therapy for Parkinson's",
                            "organization": {"name": "Test Hospital"},
                            "startDateStruct": {"year": 2020}
                        },
                        "designModule": {},
                        "conditionsModule": {},
                        "armsInterventionsModule": {
                            "interventions": [{"type": "Behavioral"}]
                        },
                        "outcomesModule": {
                            "primaryOutcomes": [{"measure": "Gait Speed"}]
                        }
                    }
                }
            ]
        }
        resp.raise_for_status.return_value = None
        mock_get.return_value = resp
        
        result = client.search("music therapy")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["study_id"] == "clinicaltrials_NCT12345678"

def test_search_handles_empty_results(client):
    """Test that search handles empty results"""
    with patch("requests.get") as mock_get:
        resp = MagicMock()
        resp.json.return_value = {"studies": []}
        resp.raise_for_status.return_value = None
        mock_get.return_value = resp
        
        result = client.search("nonexistent")
        assert result == []
```

- [ ] **Step 3: Run tests**

```bash
cd backend
python -m pytest tests/test_clinicaltrials.py -v
```

Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add backend/app/integrations/clinicaltrials.py backend/tests/test_clinicaltrials.py
git commit -m "feat: implement ClinicalTrials.gov API client"
```

---

### Task 5: Build Evidence Ingestion Service

**Files:**
- Create: `backend/app/services.py`
- Modify: `backend/app/models.py` (add Evidence.from_dict classmethod)

**Interfaces:**
- Consumes: `PubMedClient.search()`, `ClinicalTrialsClient.search()`
- Produces: `Evidence.from_dict(data: dict) -> Evidence` and `ingest_evidence(studies: List[dict], db: Session) -> int` (returns count inserted)

- [ ] **Step 1: Write backend/app/services.py**

```python
from sqlalchemy.orm import Session
from app.models import Evidence
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def ingest_evidence(studies: List[Dict], db: Session) -> int:
    """Ingest a list of studies into the database, skip duplicates"""
    count = 0
    for study in studies:
        try:
            # Check if already exists
            existing = db.query(Evidence).filter(
                Evidence.study_id == study["study_id"]
            ).first()
            
            if existing:
                logger.info(f"Skipping duplicate: {study['study_id']}")
                continue
            
            evidence = Evidence(
                study_id=study["study_id"],
                title=study.get("title", ""),
                authors=study.get("authors", ""),
                year=study.get("year"),
                intervention_type=study.get("intervention_type"),
                intervention_details=study.get("intervention_details"),
                outcomes=study.get("outcomes"),
                sample_size=study.get("sample_size"),
                effect_size=study.get("effect_size"),
                source=study.get("source", ""),
                url=study.get("url", ""),
            )
            db.add(evidence)
            count += 1
        except Exception as e:
            logger.error(f"Error ingesting {study.get('study_id')}: {e}")
    
    db.commit()
    logger.info(f"Ingested {count} new evidence records")
    return count
```

- [ ] **Step 2: Run test for duplicate handling**

```bash
cd backend
python -c "
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Evidence
from app.services import ingest_evidence

# In-memory DB for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

studies = [
    {'study_id': 'test_1', 'title': 'Study 1', 'source': 'pubmed'},
    {'study_id': 'test_1', 'title': 'Study 1', 'source': 'pubmed'},  # duplicate
]

count = ingest_evidence(studies, db)
assert count == 1, f'Expected 1 inserted, got {count}'
print('✓ Duplicate handling works')
"
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/services.py
git commit -m "feat: add evidence ingestion service with duplicate detection"
```

---

### Task 6: Build FastAPI Routes & Web API

**Files:**
- Create: `backend/app/schemas.py`
- Create: `backend/app/api/routes.py`
- Modify: `backend/app/main.py`

**Interfaces:**
- Consumes: `ingest_evidence()`, `Evidence` model
- Produces: HTTP GET `/evidence` (paginated list), GET `/evidence/search?q=...`, GET `/evidence/stats`

- [ ] **Step 1: Write backend/app/schemas.py (Pydantic models)**

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvidenceBase(BaseModel):
    title: str
    authors: Optional[str] = None
    year: Optional[int] = None
    intervention_type: Optional[str] = None
    outcomes: Optional[str] = None
    sample_size: Optional[int] = None
    effect_size: Optional[float] = None
    source: str
    url: Optional[str] = None

class EvidenceCreate(EvidenceBase):
    study_id: str

class Evidence(EvidenceBase):
    id: int
    study_id: str
    date_added: datetime
    
    class Config:
        from_attributes = True

class EvidenceListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[Evidence]

class StatsResponse(BaseModel):
    total_studies: int
    by_source: dict
    by_year: dict
    by_intervention: dict
```

- [ ] **Step 2: Write backend/app/api/routes.py**

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Evidence
from app.schemas import EvidenceListResponse, Evidence as EvidenceSchema, StatsResponse

router = APIRouter(prefix="/api", tags=["evidence"])

@router.get("/evidence", response_model=EvidenceListResponse)
async def list_evidence(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all evidence with pagination"""
    total = db.query(Evidence).count()
    skip = (page - 1) * page_size
    
    results = db.query(Evidence).offset(skip).limit(page_size).all()
    
    return EvidenceListResponse(
        total=total,
        page=page,
        page_size=page_size,
        results=[EvidenceSchema.from_orm(r) for r in results]
    )

@router.get("/evidence/search", response_model=EvidenceListResponse)
async def search_evidence(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Search evidence by title, authors, or outcomes"""
    total = db.query(Evidence).filter(
        (Evidence.title.ilike(f"%{q}%")) |
        (Evidence.authors.ilike(f"%{q}%")) |
        (Evidence.outcomes.ilike(f"%{q}%"))
    ).count()
    
    skip = (page - 1) * page_size
    results = db.query(Evidence).filter(
        (Evidence.title.ilike(f"%{q}%")) |
        (Evidence.authors.ilike(f"%{q}%")) |
        (Evidence.outcomes.ilike(f"%{q}%"))
    ).offset(skip).limit(page_size).all()
    
    return EvidenceListResponse(
        total=total,
        page=page,
        page_size=page_size,
        results=[EvidenceSchema.from_orm(r) for r in results]
    )

@router.get("/evidence/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get aggregate statistics about evidence base"""
    total = db.query(Evidence).count()
    
    by_source = dict(db.query(
        Evidence.source,
        func.count(Evidence.id)
    ).group_by(Evidence.source).all())
    
    by_year = dict(db.query(
        Evidence.year,
        func.count(Evidence.id)
    ).group_by(Evidence.year).all())
    
    by_intervention = dict(db.query(
        Evidence.intervention_type,
        func.count(Evidence.id)
    ).group_by(Evidence.intervention_type).all())
    
    return StatsResponse(
        total_studies=total,
        by_source=by_source,
        by_year=by_year,
        by_intervention=by_intervention
    )
```

- [ ] **Step 3: Write backend/app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Harmony Research API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000", "127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 4: Run backend**

```bash
cd backend
python -m uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas.py backend/app/api/routes.py backend/app/main.py
git commit -m "feat: implement FastAPI routes for evidence listing, search, stats"
```

---

### Task 7: Build React Web UI

**Files:**
- Create: `web/src/types/Evidence.ts`
- Create: `web/src/services/api.ts`
- Create: `web/src/components/SearchForm.tsx`
- Create: `web/src/components/EvidenceTable.tsx`
- Create: `web/src/App.tsx`
- Create: `web/src/main.tsx`
- Create: `web/index.html`
- Create: `web/vite.config.ts`

**Interfaces:**
- Consumes: `GET /api/evidence`, `GET /api/evidence/search`, `GET /api/evidence/stats`
- Produces: Web UI with search, table, pagination, stats

- [ ] **Step 1: Write web/src/types/Evidence.ts**

```typescript
export interface Evidence {
  id: number;
  study_id: string;
  title: string;
  authors?: string;
  year?: number;
  intervention_type?: string;
  outcomes?: string;
  sample_size?: number;
  effect_size?: number;
  source: string;
  url?: string;
  date_added: string;
}

export interface EvidenceListResponse {
  total: number;
  page: number;
  page_size: number;
  results: Evidence[];
}

export interface StatsResponse {
  total_studies: number;
  by_source: Record<string, number>;
  by_year: Record<number, number>;
  by_intervention: Record<string, number>;
}
```

- [ ] **Step 2: Write web/src/services/api.ts**

```typescript
import axios from "axios";
import { Evidence, EvidenceListResponse, StatsResponse } from "../types/Evidence";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

export const evidenceAPI = {
  list: (page: number = 1, pageSize: number = 20) =>
    api.get<EvidenceListResponse>("/evidence", { params: { page, page_size: pageSize } }),
  
  search: (query: string, page: number = 1, pageSize: number = 20) =>
    api.get<EvidenceListResponse>("/evidence/search", { params: { q: query, page, page_size: pageSize } }),
  
  stats: () =>
    api.get<StatsResponse>("/evidence/stats"),
};
```

- [ ] **Step 3: Write web/src/components/SearchForm.tsx**

```typescript
import { useState } from "react";

interface SearchFormProps {
  onSearch: (query: string) => void;
}

export function SearchForm({ onSearch }: SearchFormProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <input
        type="text"
        placeholder="Search evidence (title, authors, outcomes)..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          padding: "10px",
          width: "100%",
          maxWidth: "500px",
          marginRight: "10px",
        }}
      />
      <button type="submit" style={{ padding: "10px 20px" }}>
        Search
      </button>
    </form>
  );
}
```

- [ ] **Step 4: Write web/src/components/EvidenceTable.tsx**

```typescript
import { Evidence, EvidenceListResponse } from "../types/Evidence";

interface EvidenceTableProps {
  data: EvidenceListResponse | null;
  isLoading: boolean;
  onPageChange: (page: number) => void;
}

export function EvidenceTable({ data, isLoading, onPageChange }: EvidenceTableProps) {
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!data || data.results.length === 0) {
    return <div>No evidence found.</div>;
  }

  return (
    <div>
      <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: "20px" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #ccc" }}>
            <th style={{ padding: "10px", textAlign: "left" }}>Title</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Authors</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Year</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Intervention</th>
            <th style={{ padding: "10px", textAlign: "left" }}>Source</th>
          </tr>
        </thead>
        <tbody>
          {data.results.map((ev) => (
            <tr key={ev.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "10px" }}>
                <a href={ev.url} target="_blank" rel="noopener noreferrer">
                  {ev.title}
                </a>
              </td>
              <td style={{ padding: "10px", fontSize: "0.9em" }}>{ev.authors || "—"}</td>
              <td style={{ padding: "10px" }}>{ev.year || "—"}</td>
              <td style={{ padding: "10px", fontSize: "0.9em" }}>{ev.intervention_type || "—"}</td>
              <td style={{ padding: "10px" }}>{ev.source}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={() => onPageChange(data.page - 1)}
          disabled={data.page === 1}
          style={{ marginRight: "10px" }}
        >
          Previous
        </button>
        <span>
          Page {data.page} of {Math.ceil(data.total / data.page_size)}
        </span>
        <button
          onClick={() => onPageChange(data.page + 1)}
          disabled={data.page * data.page_size >= data.total}
          style={{ marginLeft: "10px" }}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

- [ ] **Step 5: Write web/src/App.tsx**

```typescript
import { useState, useEffect } from "react";
import { SearchForm } from "./components/SearchForm";
import { EvidenceTable } from "./components/EvidenceTable";
import { evidenceAPI } from "./services/api";
import { EvidenceListResponse, StatsResponse } from "./types/Evidence";

function App() {
  const [data, setData] = useState<EvidenceListResponse | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadStats();
    loadEvidence();
  }, []);

  const loadStats = async () => {
    try {
      const resp = await evidenceAPI.stats();
      setStats(resp.data);
    } catch (err) {
      console.error("Failed to load stats:", err);
    }
  };

  const loadEvidence = async (query?: string, page: number = 1) => {
    setIsLoading(true);
    try {
      const resp = query
        ? await evidenceAPI.search(query, page)
        : await evidenceAPI.list(page);
      setData(resp.data);
      setCurrentPage(page);
    } catch (err) {
      console.error("Failed to load evidence:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1);
    loadEvidence(query, 1);
  };

  const handlePageChange = (page: number) => {
    loadEvidence(searchQuery || undefined, page);
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "20px" }}>
      <h1>Harmony Research: Evidence Aggregator</h1>

      {stats && (
        <div style={{ marginBottom: "20px", padding: "10px", backgroundColor: "#f5f5f5" }}>
          <p><strong>Total Studies:</strong> {stats.total_studies}</p>
          <p><strong>By Source:</strong> {JSON.stringify(stats.by_source)}</p>
        </div>
      )}

      <SearchForm onSearch={handleSearch} />

      <EvidenceTable
        data={data}
        isLoading={isLoading}
        onPageChange={handlePageChange}
      />
    </div>
  );
}

export default App;
```

- [ ] **Step 6: Write web/src/main.tsx**

```typescript
import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App.tsx"
import "./styles/App.css"

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

- [ ] **Step 7: Write web/index.html**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Harmony Research</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 8: Write web/vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
})
```

- [ ] **Step 9: Write web/tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForModule": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 10: Write web/src/styles/App.css**

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  line-height: 1.5;
  color: #333;
  background-color: #fafafa;
}

h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

a {
  color: #0066cc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f5f5f5;
  padding: 8px 16px;
}

button:hover {
  background-color: #e8e8e8;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input[type="text"] {
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}
```

- [ ] **Step 11: Commit**

```bash
git add web/src/ web/index.html web/vite.config.ts web/tsconfig.json
git commit -m "feat: build react web ui for evidence browsing and search"
```

---

### Task 8: Integration Test & Initial Release

**Files:**
- Create: `backend/tests/test_integration.py`
- Modify: `README.md` (add setup and quick start)

- [ ] **Step 1: Write backend/tests/test_integration.py**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, Evidence
from app.database import get_db

# In-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def seed_data():
    """Seed test data before each test"""
    db = TestingSessionLocal()
    test_evidence = [
        Evidence(
            study_id="test_1",
            title="Music Therapy for Parkinson's",
            authors="Smith, J.",
            year=2020,
            intervention_type="music_pt",
            outcomes="gait",
            source="pubmed",
            url="http://example.com"
        ),
        Evidence(
            study_id="test_2",
            title="Rhythm and Motor Control",
            authors="Jones, A.",
            year=2021,
            intervention_type="music_alone",
            outcomes="fine_motor",
            source="clinicaltrials",
            url="http://example.com"
        ),
    ]
    for ev in test_evidence:
        db.add(ev)
    db.commit()
    yield
    db.query(Evidence).delete()
    db.commit()

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_evidence():
    """Test GET /api/evidence"""
    response = client.get("/api/evidence")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["results"]) == 2

def test_search_evidence():
    """Test GET /api/evidence/search"""
    response = client.get("/api/evidence/search?q=Parkinson")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert "Parkinson" in data["results"][0]["title"]

def test_stats():
    """Test GET /api/evidence/stats"""
    response = client.get("/api/evidence/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_studies"] == 2
    assert data["by_source"]["pubmed"] == 1
    assert data["by_source"]["clinicaltrials"] == 1

def test_pagination():
    """Test pagination on list endpoint"""
    response = client.get("/api/evidence?page=1&page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["page"] == 1
```

- [ ] **Step 2: Run integration tests**

```bash
cd backend
python -m pytest tests/test_integration.py -v
```

Expected: PASS (all tests)

- [ ] **Step 3: Update README.md with quickstart**

```markdown
# Harmony Research: Evidence Aggregator

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations
alembic upgrade head

# Start API
uvicorn app.main:app --reload
```

### Web UI Setup

```bash
cd web
npm install
npm run dev
# Visit http://localhost:3000
```

### Ingest Evidence (CLI)

```python
from app.integrations.pubmed import PubMedClient
from app.integrations.clinicaltrials import ClinicalTrialsClient
from app.services import ingest_evidence
from app.database import SessionLocal

db = SessionLocal()

# Search PubMed
pubmed = PubMedClient()
pubmed_results = pubmed.search("music therapy parkinson", max_results=50)
ingest_evidence(pubmed_results, db)

# Search ClinicalTrials.gov
ct = ClinicalTrialsClient()
ct_results = ct.search("music parkinson", max_results=50)
ingest_evidence(ct_results, db)

print(f"Ingested {len(pubmed_results) + len(ct_results)} studies")
```

## API Endpoints

- `GET /health` — Health check
- `GET /api/evidence` — List all evidence (paginated)
- `GET /api/evidence/search?q=...` — Search evidence
- `GET /api/evidence/stats` — Aggregate statistics

## Phase 1 Status

- ✅ Evidence database schema
- ✅ PubMed integration
- ✅ ClinicalTrials.gov integration
- ✅ Evidence ingestion service
- ✅ Web API (FastAPI)
- ✅ React web UI
- ✅ Integration tests

## Next (Phase 2)

- Gap finder: AI analysis to identify unexplored music + outcome combinations
- Enhanced evidence extraction: use NLP to categorize music properties and outcomes
```

- [ ] **Step 4: Create CHANGELOG.md**

```markdown
# Changelog

## [0.1.0] - 2026-10-17

### Added
- Evidence database with PostgreSQL
- PubMed API integration for literature search
- ClinicalTrials.gov API integration
- FastAPI backend with RESTful endpoints
- React web UI for evidence browsing and search
- Pagination and full-text search on evidence
- Aggregate statistics endpoint
- Integration tests

### Phase 1 Complete
- Evidence aggregator MVP
- Public data ingestion from PubMed and ClinicalTrials.gov
- Web interface for researchers
```

- [ ] **Step 5: Final commit and tag**

```bash
git add README.md CHANGELOG.md
git commit -m "docs: add quickstart and API documentation"
git tag -a v0.1.0 -m "Evidence aggregator MVP"
git log --oneline | head -10
```

---

## Summary

**Phase 1 Complete.** You now have:

- ✅ PostgreSQL evidence database with schema
- ✅ PubMed scraper (100+ papers searchable)
- ✅ ClinicalTrials.gov scraper
- ✅ FastAPI backend with search/filter/stats
- ✅ React web UI with pagination
- ✅ Integration tests
- ✅ GitHub repo with v0.1.0 release
- ✅ Full documentation

**Timeline:** ~4 weeks for Phase 1 (one person, part-time)

**Next:** Phase 2 (months 4–8) builds the gap finder using scientific-agent-skills NLP + hypothesis generation.