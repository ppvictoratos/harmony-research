# Harmony Research — Project Summary

**Status:** Phase 1 Implementation Plan Ready  
**Timeline:** 24 months (4 phases)  
**Goal:** Discover musical elements that improve Parkinson's outcomes through evidence aggregation, gap analysis, and experiment design.

---

## What We've Built So Far

### 0. Research Foundation ✅
**Psychoacoustics** — Foundational theory explaining how sound perception drives motor and emotional responses in Parkinson's patients. Guides which musical properties (rhythm, pitch, timbre, tonality) to research and why.

📄 See: `docs/research-foundation/psychoacoustics.md`

### 1. Architectural Design ✅
Complete 24-month system design covering:
- **Web Research Platform** (TypeScript/React) — evidence aggregator, gap finder, experiment designer
- **iOS App** (Swift) — therapist session tracking and data capture
- **Python Backend** (scientific-agent-skills) — analysis and research workflows
- **Four Phases** — evidence aggregator (phase 1), gap finder (phase 2), experiment designer + iOS app (phase 3), publication (phase 4)

📄 See: `docs/design/music-therapy-research-design.md`

### 2. Phase 1 Implementation Plan ✅
Detailed task breakdown for building the Evidence Aggregator MVP (months 1–4):
- Task 1: GitHub repo setup
- Task 2: PostgreSQL database schema
- Task 3: PubMed API integration
- Task 4: ClinicalTrials.gov API integration
- Task 5: Evidence ingestion service
- Task 6: FastAPI backend routes
- Task 7: React web UI
- Task 8: Integration tests + v0.1.0 release

**Deliverable:** Fully functional evidence aggregator pulling from PubMed and ClinicalTrials.gov, with web UI for browsing/searching.

📄 See: `docs/plans/2026-10-17-music-therapy-phase1-plan.md`

---

## Tech Stack

| Layer | Tech | Version |
|-------|------|---------|
| Backend API | FastAPI | 0.104+ |
| Database | PostgreSQL | 14+ |
| Web Frontend | React + TypeScript | 18+ |
| iOS App | Swift + SwiftUI | (Phase 3) |
| Python Runtime | Python | 3.11+ |
| Testing | pytest + vitest | latest |
| Deployment | GitHub | public repo |

---

## Next Steps: Getting Started on Your Other Machine

### Prerequisites
```bash
# Ensure you have:
- Python 3.11+ (check: python --version)
- PostgreSQL 14+ running locally (brew services start postgresql)
- Node.js 18+ (check: node --version)
- Git
```

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/harmony-research.git
cd harmony-research

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .
pip install -r requirements.txt

# 3. Create .env and configure database
cp .env.example .env
# Edit .env — set DATABASE_URL to your PostgreSQL connection string
# Example: postgresql://user:password@localhost:5432/harmony_db

# 4. Run migrations
alembic upgrade head

# 5. Start API server (in one terminal)
uvicorn app.main:app --reload
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs

# 6. Web UI setup (in another terminal)
cd ../web
npm install
npm run dev
# UI available at http://localhost:3000
```

### Ingest Initial Data

Once both servers are running, ingest research papers from PubMed and ClinicalTrials.gov:

```bash
# From backend directory (in Python shell or script)
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

Then visit http://localhost:3000 to browse the evidence base.

---

## Project Structure

```
harmony-research/
├── docs/
│   ├── design/
│   │   └── music-therapy-research-design.md (24-month architecture)
│   └── plans/
│       └── 2026-10-17-music-therapy-phase1-plan.md (Phase 1 tasks)
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── models.py (SQLAlchemy ORM)
│   │   ├── database.py (DB connection)
│   │   ├── api/routes.py (REST endpoints)
│   │   └── integrations/ (PubMed, ClinicalTrials APIs)
│   ├── tests/ (unit + integration tests)
│   ├── migrations/ (Alembic)
│   └── pyproject.toml
├── web/
│   ├── src/
│   │   ├── App.tsx (main component)
│   │   ├── components/ (SearchForm, EvidenceTable)
│   │   └── services/api.ts (API client)
│   ├── package.json
│   └── vite.config.ts
├── README.md
├── SUMMARY.md (this file)
├── LICENSE (MIT)
└── .gitignore
```

---

## Key Files to Know

- **Design Document:** `docs/design/music-therapy-research-design.md` — Read this first to understand the full vision and phases
- **Implementation Plan:** `docs/plans/2026-10-17-music-therapy-phase1-plan.md` — Step-by-step tasks with code for Phase 1
- **API Reference:** `backend/app/api/routes.py` — GET /api/evidence, /api/evidence/search, /api/evidence/stats
- **Web UI:** `web/src/App.tsx` — React component with search, table, pagination

---

## What's Working Now

✅ Database schema designed  
✅ PubMed API integration code written  
✅ ClinicalTrials.gov API integration code written  
✅ FastAPI backend routes defined  
✅ React web UI scaffolded  
✅ Integration tests written  
✅ Documentation complete  

---

## What You'll Do Next (On Your Machine)

1. Clone this repo
2. Follow **Quick Start** above
3. Run Phase 1 tasks in order (see the plan)
4. By month 4: have v0.1.0 published with 100+ research papers indexed

---

## Research Focus

We're studying:
- **Outcomes:** Gait (cadence, speed, freezing), fine motor control (dexterity, tremor), posture, speech
- **Music Elements:** Tempo (BPM), key (major/minor), chord progressions, rhythm, timbre, duration
- **Interventions:** Music alone, music + PT, music + OT, music + speech therapy

---

## Questions?

- **Architecture:** See `docs/design/music-therapy-research-design.md`
- **Implementation:** See `docs/plans/2026-10-17-music-therapy-phase1-plan.md`
- **API Endpoints:** See `backend/README.md`
- **Contributing:** Issues and PRs welcome

---

**Created:** 2026-10-17  
**Phase:** 1 of 4  
**Next Review:** Month 4 (mid-2027)
