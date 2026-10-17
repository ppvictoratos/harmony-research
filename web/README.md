# Web UI: Harmony Research Evidence Browser

React + TypeScript web interface for browsing and searching the evidence database.

## Setup

```bash
npm install
npm run dev
```

UI available at: http://localhost:3000

## Features

- **Evidence List** — Browse all indexed studies with pagination
- **Full-Text Search** — Search by title, authors, outcomes
- **Filtering** — Filter by source (PubMed, ClinicalTrials), intervention type, year
- **Statistics** — View aggregate stats (total studies, breakdown by source/intervention)
- **Links** — Direct links to original sources (PubMed, ClinicalTrials.gov)

## Components

```
src/
├── App.tsx                   # Main app component
├── main.tsx                  # React entry point
├── types/Evidence.ts         # TypeScript interfaces
├── services/api.ts           # API client
├── components/
│   ├── SearchForm.tsx        # Search input
│   ├── EvidenceTable.tsx     # Evidence list + pagination
│   └── FilterPanel.tsx       # Filter controls (future)
└── styles/App.css            # Styling
```

## Building

```bash
# Development build
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## Testing

```bash
npm run test
```

## Environment

Create `.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Phase 1 Tasks

See [../docs/plans/2026-10-17-music-therapy-phase1-plan.md](../docs/plans/2026-10-17-music-therapy-phase1-plan.md) for implementation details.

Task 7 covers the web UI.

## Next Steps

Phase 2: Add filtering, sorting, export functionality.
Phase 3: iOS-specific visualizations and deeper evidence analysis.
