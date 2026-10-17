# Backend: Harmony Research API

FastAPI-based backend for evidence aggregation and research workflows.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Create .env file
cp ../.env.example .env
# Edit .env with your DATABASE_URL

# Initialize database
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

API available at: http://localhost:8000  
API docs (Swagger): http://localhost:8000/docs

## API Endpoints

### Health
- `GET /health` — Health check

### Evidence
- `GET /api/evidence?page=1&page_size=20` — List all evidence (paginated)
- `GET /api/evidence/search?q=music&page=1` — Search evidence by title, authors, outcomes
- `GET /api/evidence/stats` — Get aggregate statistics

### Evidence Response Schema
```json
{
  "id": 1,
  "study_id": "pubmed_12345",
  "title": "Music Therapy for Parkinson's Disease",
  "authors": "Smith, J.",
  "year": 2020,
  "intervention_type": "music_pt",
  "outcomes": "gait",
  "sample_size": 50,
  "effect_size": 0.8,
  "source": "pubmed",
  "url": "https://pubmed.ncbi.nlm.nih.gov/12345/",
  "date_added": "2026-10-17T10:00:00"
}
```

## Data Ingestion

Once the API is running, ingest research papers:

```bash
python -c "
from app.integrations.pubmed import PubMedClient
from app.integrations.clinicaltrials import ClinicalTrialsClient
from app.services import ingest_evidence
from app.database import SessionLocal

db = SessionLocal()

print('Fetching from PubMed...')
pubmed = PubMedClient()
pubmed_results = pubmed.search('music therapy parkinson', max_results=50)
ingest_evidence(pubmed_results, db)

print('Fetching from ClinicalTrials.gov...')
ct = ClinicalTrialsClient()
ct_results = ct.search('music parkinson', max_results=50)
ingest_evidence(ct_results, db)

print(f'✓ Ingested {len(pubmed_results) + len(ct_results)} studies')
"
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pubmed.py -v

# Run with coverage
pytest --cov=app tests/
```

## Architecture

```
app/
├── main.py              # FastAPI app initialization
├── models.py            # SQLAlchemy ORM (Evidence table)
├── schemas.py           # Pydantic request/response models
├── database.py          # Database connection and session
├── config.py            # Configuration (env vars)
├── services.py          # Business logic (ingestion, etc.)
├── api/
│   └── routes.py        # REST endpoints
└── integrations/
    ├── pubmed.py        # PubMed E-utilities client
    └── clinicaltrials.py # ClinicalTrials.gov API client
```

## Phase 1 Tasks

See [../docs/plans/2026-10-17-music-therapy-phase1-plan.md](../docs/plans/2026-10-17-music-therapy-phase1-plan.md) for detailed implementation steps.

Tasks 1–6 are backend-focused:
1. ✅ GitHub repo setup
2. ✅ Database schema + migrations
3. ✅ PubMed API integration
4. ✅ ClinicalTrials.gov integration
5. ✅ Evidence ingestion service
6. ✅ FastAPI routes

## Database

Uses PostgreSQL with SQLAlchemy ORM.

**Evidence Table:**
- `id` (primary key)
- `study_id` (unique)
- `title`, `authors`, `year`
- `intervention_type`, `intervention_details` (JSON)
- `outcomes`, `sample_size`, `effect_size`
- `source` (pubmed, clinicaltrials)
- `url`
- `date_added`, `created_at` (timestamps)

## Next Steps

Phase 2: Implement gap finder using scientific-agent-skills for hypothesis generation.
