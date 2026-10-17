# Harmony Research: Music Therapy + Parkinson's Evidence Platform

A research platform to discover musical elements (chord progressions, rhythms, note sequences) that improve Parkinson's outcomes through systematic evidence aggregation, gap analysis, and experiment design.

## Phase 1: Evidence Aggregator

This phase builds a web-based research tool that:
- Pulls public research from PubMed and ClinicalTrials.gov
- Structures findings into a searchable evidence database
- Provides a web UI for researchers to browse, search, and filter evidence
- Tracks intervention types (music + PT, music alone, etc.) and outcomes (gait, motor control, mood, etc.)

## Getting Started

**See [SUMMARY.md](SUMMARY.md) for quickstart instructions.**

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Node.js 18+

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
alembic upgrade head
uvicorn app.main:app --reload
```

### Web UI
```bash
cd web
npm install
npm run dev
```

Visit http://localhost:3000 to browse evidence.

## Project Structure

```
harmony-research/
├── docs/
│   ├── design/music-therapy-research-design.md
│   └── plans/2026-10-17-music-therapy-phase1-plan.md
├── backend/
│   ├── app/
│   ├── tests/
│   └── pyproject.toml
├── web/
│   ├── src/
│   └── package.json
├── SUMMARY.md
├── README.md
└── LICENSE
```

## Key Documents

- **[SUMMARY.md](SUMMARY.md)** — Project overview and quickstart
- **[docs/design/music-therapy-research-design.md](docs/design/music-therapy-research-design.md)** — Full 24-month architecture
- **[docs/plans/2026-10-17-music-therapy-phase1-plan.md](docs/plans/2026-10-17-music-therapy-phase1-plan.md)** — Phase 1 implementation tasks

## Research Foundation

This project is grounded in **psychoacoustics**—the study of how the human auditory system perceives and responds to sound. Understanding psychoacoustics is key to explaining *why* certain music properties (rhythm, pitch, timbre) improve motor control and mood in Parkinson's patients.

See [docs/research-foundation/psychoacoustics.md](docs/research-foundation/psychoacoustics.md) for the theoretical foundation.

## Research Scope

**Music + Parkinson's outcomes:**
- Gait (cadence, speed, freezing)
- Fine motor control (dexterity, tremor)
- Posture and balance
- Speech

**Musical elements:**
- Rhythm & tempo
- Tonality (major/minor keys, chord progressions)
- Timbre & instrumentation
- Duration and structure

**Data sources:**
- Public research only (PubMed, ClinicalTrials.gov, preprints)
- No patient data collection in Phase 1

## Timeline

- **Phase 1 (Months 1–4):** Evidence aggregator MVP ← *You are here*
- **Phase 2 (Months 4–8):** Gap finder (AI-driven analysis)
- **Phase 3 (Months 8–12):** Experiment designer + iOS app
- **Phase 4 (Months 12–24):** Real data collection, analysis, publication

## Tech Stack

| Component | Stack |
|-----------|-------|
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| Web UI | React, TypeScript, Vite |
| APIs | PubMed E-utilities, ClinicalTrials.gov API |
| Testing | pytest, vitest |
| Deployment | GitHub + local/cloud compute |

## Contributing

This project welcomes:
- Bug reports and feature requests (open an issue)
- Pull requests (especially from music therapists, Parkinson's researchers)
- Research collaboration

See [docs/plans/2026-10-17-music-therapy-phase1-plan.md](docs/plans/2026-10-17-music-therapy-phase1-plan.md) for implementation details.

## License

MIT — See [LICENSE](LICENSE)

## Contact & Feedback

- Questions? Check [SUMMARY.md](SUMMARY.md) or the design documents
- Feedback? Open an issue

---

**Status:** Phase 1 Planning  
**Last Updated:** 2026-10-17  
**Next Review:** Month 4
