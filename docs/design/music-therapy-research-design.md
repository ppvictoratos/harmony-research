# Music Therapy + Parkinson's Research Platform — Architectural Design

**Date:** 2026-10-16  
**Project Name:** Harmony Research (working title)  
**Timeline:** 24 months  
**Author:** Design brainstorm with scientific-agent-skills integration  

---

## Vision

Build an **evidence aggregator + experiment generator** that discovers musical elements (chord progressions, rhythms, note sequences) that improve Parkinson's outcomes—both in combination with physical therapy and in isolation. Use public research data to identify gaps, generate hypotheses, and guide rigorous experiment design. Publish findings to advocate for the field.

---

## System Architecture

### Three-Tier Stack

**1. Web Research Platform (TypeScript/React)**
- Evidence aggregator: pull and structure published music therapy + Parkinson's research
- Gap finder: AI-driven analysis of what's been tested, what works, what's unexplored
- Experiment designer: help structure rigorous studies based on identified gaps
- Powered by scientific-agent-skills (literature review, hypothesis generation, experimental design skills)
- Admin/researcher interface for managing the evidence base and proposing experiments

**2. iOS App (Swift)**
- Session tracker for music therapists: log sessions, music properties (tempo, chord, rhythm), patient outcomes
- Real-time data capture: what music was used, patient response, observed improvements
- Simple outcome measures (gait speed, fine motor tasks, mood, etc.)
- Upload to backend for aggregation and analysis

**3. Backend / Data Layer**
- Evidence database: structured repository of published research findings (extracted from literature, clinical trials, preprints)
- Session data store: anonymized session logs from iOS app
- Python API (integrates with scientific-agent-skills for analysis workflows)
- Integration layer: PubMed, ClinicalTrials.gov, arXiv, bioRxiv APIs

---

## Key Components

### Web Platform

**Evidence Aggregator**
- Automated literature ingestion: PubMed, ClinicalTrials.gov, bioRxiv, medRxiv, arXiv
- Structured extraction: what musical elements tested, what outcomes measured, sample size, effect sizes
- Evidence database: queryable, filterable, versioned
- Manual review + curation (you + collaborators)

**Gap Finder**
- AI analysis (powered by scientific-agent-skills): what combinations of music + intervention haven't been tested?
- Patterns: e.g., "Major vs. minor chords for fine motor control—tested for PT combination but not alone"
- Ranking: suggest highest-potential gaps to test next (based on mechanistic reasoning + publication trends)
- Provenance: show *why* something is flagged as a gap (which studies are missing, which outcomes underexplored)

**Experiment Designer**
- Templates for rigorous studies (RCT, quasi-experimental, within-subject)
- Guidance from scientific-agent-skills: sample size calculation, blinding strategies, outcome selection
- Hypothesis generation: what does the evidence base suggest you should test?
- Protocol drafting: auto-generate study protocol outline based on gap + selected design

### iOS App

**Session Tracking**
- Therapist selects or logs: patient (anonymized ID), music properties (tempo BPM, key/chord, rhythm pattern, duration)
- Records outcomes: gait speed (timed walk), fine motor (pegboard, buttons), mood, pain, fatigue (simple scales)
- Optional: audio capture (for later analysis of music properties if needed)
- Sync to backend (encrypted, anonymized)

**Data Visualization**
- Personal session history (therapist/researcher can see trends)
- Aggregate patterns: "patients who used X rhythm showed Y improvement"
- Export for analysis

### Backend / Analysis Layer

**Python API**
- Exposes scientific-agent-skills workflows:
  - Literature review: search, summarize, extract key findings
  - Experimental design: help structure protocols
  - Statistical analysis: analyze session data for patterns
- Data validation and aggregation
- Scheduling: background jobs to re-analyze evidence base as new data arrives

**Data Storage**
- PostgreSQL (or similar): research metadata, session logs
- Versioned evidence base: track what research exists, when it was added, provenance

---

## Research Scope & Focus

### Theoretical Foundation: Psychoacoustics

This research is grounded in **psychoacoustics**—the study of how the human auditory system perceives and responds to sound. Music's therapeutic effects on Parkinson's motor control operate through auditory-motor coupling: rhythmic music provides external temporal cues that engage motor pathways through the cerebellum and premotor cortex, effectively bypassing the damaged basal ganglia circuits that cause bradykinesia and rigidity.

The psychoacoustic properties we track—rhythm/tempo, pitch/tonality, timbre, and complexity—each have different effects on auditory processing and motor engagement. By understanding these mechanisms, we can identify which specific musical elements work best for which Parkinson's symptoms.

**See:** [../research-foundation/psychoacoustics.md](../research-foundation/psychoacoustics.md) for detailed theory and research questions this informs.

### What We're Studying (Broad)

**Music + Parkinson's motor outcomes:**
- Gait (cadence, speed, freezing episodes)
- Fine motor control (dexterity, tremor, coordination)
- Posture and balance
- Speech (if relevant)

**Musical Elements:**
- Rhythm: tempo (BPM), beat complexity, polyrhythm
- Tonality: major vs. minor keys, chord progressions, dissonance
- Timbre: instrument types, harmonicity
- Duration and structure: session length, phrasing

**Intervention Combinations:**
- Music alone
- Music + physical therapy
- Music + occupational therapy
- Music + speech therapy (if data exists)
- Music + medication (correlational from existing studies)

### What We're NOT Doing (Scope Boundaries)

- Patient recruitment or primary data collection (Phase 1–3)
- Real-time music generation or clinical deployment (iOS is tracking + feedback, not therapy device)
- Diagnostic or treatment recommendations
- Any work requiring IRB approval for new studies (focus on synthesis + design, not execution early on)

---

## Phase Breakdown (24 Months)

### Phase 1: Evidence Aggregator MVP (Months 1–4)

**Goals:**
- Pull public research on music therapy + Parkinson's
- Structure findings into a queryable evidence base
- Establish data model for what we track

**Deliverables:**
- Evidence database schema (what fields we extract from papers)
- Scraper/ingestion for PubMed, ClinicalTrials.gov (100+ papers on music + Parkinson's)
- Web UI to browse and filter evidence
- GitHub repo with phase 1 code, README, example data
- Published: v0.1 on GitHub (evidence aggregator alpha)

**Technical:**
- TypeScript/React for web UI
- Python backend (scientific-agent-skills integration)
- PostgreSQL for evidence store
- PubMed API, ClinicalTrials.gov API integrations

**Team:**
- You: full implementation
- Wife: consultation on what research fields matter, evidence quality assessment

---

### Phase 2: Gap Finder (Months 4–8)

**Goals:**
- Analyze the evidence base: what's been tested, what's missing
- Use AI (scientific-agent-skills) to generate gap hypotheses
- Rank promising unexplored combinations

**Deliverables:**
- Gap analysis engine: identifies underexplored music + outcome combinations
- Hypothesis generation: system suggests "minor chords + fine motor," "polyrhythm + gait," etc.
- Web UI: browse gaps, see reasoning (which studies support/refute the gap claim)
- GitHub: v0.2 (gap finder)

**Technical:**
- Integrate scientific-agent-skills: hypothesis-generation and research-methodology skills
- NLP/embedding layer to compare studies semantically (identify duplicates, related work)
- Ranking algorithm: score gaps by novelty, mechanistic plausibility, existing effect sizes
- Visualizations: gap heatmaps (music element × outcome)

**Team:**
- You: implementation
- Wife: validate that gaps align with what researchers would actually care about

---

### Phase 3: Experiment Designer + iOS App (Months 8–12)

**Goals:**
- Help design rigorous experiments to test identified gaps
- iOS app for therapists to start collecting outcome data
- Proof-of-concept data pipeline

**Deliverables:**
- Experiment designer: templates, sample-size calculation, protocol drafting (powered by scientific-agent-skills)
- iOS app (Swift): session logging, outcome tracking, sync to backend
- Example protocol: "Test minor vs. major chord progressions for fine motor control"
- GitHub: v0.3 (experiment designer + iOS alpha)
- First therapy partner? (if available)

**Technical:**
- Experiment designer: uses scientific-agent-skills experimental-design skill
- iOS: SwiftUI, local storage, encrypted sync
- Backend: session ingestion, validation, aggregation endpoints
- Analytics: early dashboards on session data

**Team:**
- You: full implementation
- Wife: design experiments with scientific rigor
- (Optional) 1–2 music therapist partners: test iOS app, provide feedback

---

### Phase 4: Iteration, Analysis & Publication (Months 12–24)

**Goals:**
- Analyze early session data from iOS app (if collected)
- Refine gap finder based on real-world experiments
- Publish findings (blog, preprint, GitHub)
- Community building

**Deliverables:**
- v1.0: stable evidence aggregator, gap finder, experiment designer
- Publication: preprint (bioRxiv) or paper on music + Parkinson's gaps found
- Blog series: "What music therapy research is missing," case studies
- GitHub: organized, documented, ready for contributors
- (Optional) Open-source the scientific-agent-skills fork with music-therapy-specific skills

**Technical:**
- Data analysis: run statistical workflows on collected session data (scientific-agent-skills stats skills)
- Refinement: gap finder learns from real experiments
- iOS v1: stability, more outcome measures, better visualization

**Team:**
- You: development + writing
- Wife: research analysis + publication strategy
- Community: feedback, contributions

---

## Integration with Scientific Agent Skills

**How it powers the platform:**

1. **Literature Review Skill**
   - Automated PubMed/arXiv searching and summarization
   - Extract structured fields: intervention, outcome, sample, effect size
   - Detect duplicates and related work

2. **Hypothesis Generation Skill**
   - Suggest research gaps based on evidence base coverage
   - Reason about what combinations are mechanistically plausible
   - Rank gaps by novelty and potential impact

3. **Experimental Design Skill**
   - Help structure study protocols (RCT, quasi-experimental, within-subject)
   - Sample-size calculation
   - Outcome selection guidance
   - Blinding and control strategies

4. **Statistical Analysis Skill**
   - Analyze session data from iOS app
   - Identify patterns: which music elements correlate with better outcomes
   - Effect size estimation

5. **Scientific Writing Skill**
   - Auto-generate first drafts of findings
   - Support publication-ready reports

**Fork Strategy:**
- Fork scientific-agent-skills
- Add music-therapy-specific skills (optional Phase 4+):
  - Music property analysis (extract tempo, key, rhythm from audio or notation)
  - Parkinson's-specific outcome interpretation
  - Therapy protocol templates

---

## Music Generation (Endel Integration)

**Phase 1–3:** Endel is a reference/inspiration layer—you study what Endel's approach is, but don't integrate it yet.

**Phase 4+:** Once you've identified which music properties work, could partner with Endel or build a simple generator that:
- Takes learned rules ("minor chords + 100 BPM rhythm → better gait")
- Generates therapeutic sessions
- iOS app uses generated music in real sessions

**Decision point:** Reassess in month 12 based on findings.

---

## GitHub & Open Source

**Repository Structure:**
```
harmony-research/
├── README.md (vision, setup, contributing)
├── web/ (TypeScript/React research platform)
├── ios/ (Swift app)
├── backend/ (Python API + scientific-agent-skills integration)
├── data/ (example evidence exports, public datasets)
├── docs/ (research findings, blog posts, design decisions)
├── scientific-agent-skills-fork/ (your fork with music-therapy skills)
└── LICENSE (MIT)
```

**Publishing Schedule:**
- Month 4: v0.1 (evidence aggregator alpha)
- Month 8: v0.2 (gap finder)
- Month 12: v0.3 (experiment designer + iOS)
- Month 24: v1.0 + publication

**Community:**
- GitHub discussions: research questions, gap suggestions
- Issues: feature requests, bug reports
- Contributions: pull requests welcome (especially from music therapists, Parkinson's researchers)

---

## Success Criteria

**By Month 12:**
- Evidence base contains 200+ published studies on music + Parkinson's
- Gap finder identifies 10+ unexplored music + outcome combinations
- Experiment designer helps draft a rigorous protocol
- iOS app is alpha-tested by 2–3 therapists
- 50+ stars on GitHub

**By Month 24:**
- 500+ studies in evidence base
- Real therapy session data (from 5+ therapists, 20+ sessions minimum)
- Published findings: at least one blog post + preprint showing which music properties + outcomes are underexplored
- 300+ GitHub stars, small community

---

## Open Questions & Decision Points

1. **Music + PT vs. music alone focus:** Should early phases focus on PT combinations, or cast wider net? → *Current plan: both, but PT + music likely has more research already, so start there*

2. **Primary data collection timeline:** When do you want to recruit therapists and start collecting iOS session data? → *Current plan: month 8 (Phase 3), but can move earlier if opportunities exist*

3. **Endel partnership:** Reach out for collaboration, or build independently first? → *Current plan: month 12 assessment*

4. **Publication strategy:** Preprint first, then peer-reviewed journal? Blog and Twitter for advocacy? → *Wife's input critical here*

5. **Contributor onboarding:** When/how do you invite collaborators (other researchers, developers)? → *After v0.2 (month 8), probably*

---

## Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│                  Web Research Platform (TypeScript/React)   │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Evidence        │  │ Gap Finder   │  │ Experiment     │ │
│  │ Aggregator      │  │ (AI-driven)  │  │ Designer       │ │
│  └────────┬────────┘  └──────┬───────┘  └────────┬───────┘ │
└───────────┼──────────────────┼─────────────────────┼────────┘
            │                  │                     │
            └──────────────────┼─────────────────────┘
                               │
                   ┌───────────▼──────────┐
                   │   Python API         │
                   │ (Scientific Agent    │
                   │  Skills Integration) │
                   └───────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
         ┌──────▼──────┐ ┌────▼─────┐ ┌────▼─────┐
         │ PostgreSQL  │ │ PubMed   │ │iOS App   │
         │ (Evidence & │ │ Clinical │ │(Swift)   │
         │ Sessions)   │ │Trials API│ │          │
         └─────────────┘ └──────────┘ └──────────┘
```

---

## Next Steps (If Approved)

1. ✅ Design reviewed and approved by you
2. → Invoke writing-plans skill to break this into implementation tasks
3. → Create GitHub repo with initial structure
4. → Start Phase 1 (evidence aggregator)
