# From personal tool to something clinicians can use

**Status:** exploration · **Written:** 2026-10-22

Today Harmony Research is a single-user app on one laptop: an evidence browser plus a personal n-of-1 study builder. This document maps what it would take for music therapists, physical therapists, researchers and other individuals to use it, and in what order.

## Who would use it, and for what

| Who | What they'd do | What they need that's missing today |
|---|---|---|
| **Individuals** (like me) | Run their own n-of-1 study on mood or focus | Hosted app or easy install, accounts, phone-friendly logging, reminders |
| **Music therapists / neurologic music therapists** | Track a client's sessions; compare approaches (tempo, instrument, active vs receptive) | Multiple clients per therapist, validated outcome measures, session protocols, exportable progress reports |
| **Physical / speech therapists** | Rhythmic auditory cueing for gait; singing for speech in Parkinson's | Measures like gait speed, cadence, Timed Up and Go; BPM relative to the patient's cadence |
| **Researchers** | Run a "series of n-of-1" study across many participants; find gaps in the evidence | Multi-participant protocols, consent tracking, data export (CSV, REDCap), proper statistics, audit trail |

**Recommendation:** start with **music therapists**. They are the closest fit to what already exists, they decide session content themselves, and a working therapist's feedback will sharpen everything else. Individuals come along almost for free.

## The big decision: patient data

The moment a clinician enters information about a client, the app may be holding **protected health information (PHI)**. In the US that brings HIPAA: encryption, access controls, audit logs, breach procedures, and a Business Associate Agreement (BAA) with every vendor that touches the data (hosting, database, email).

Three ways to handle it, from lightest to heaviest:

1. **Local-first / self-hosted.** Each clinic runs its own copy (like today's `dev.sh`, but packaged). Data never leaves their machine or network. Cheapest and simplest; the clinic owns compliance. Weak for sharing and backups.
2. **De-identified hosted.** Clients are pseudonyms or codes (e.g. "Client 07"), with no names, dates of birth or contact details. Much lower risk, though not zero: free-text notes can still identify people, so they need guidance or limits.
3. **Full HIPAA-compliant hosted.** Proper SaaS with BAAs (e.g. AWS, GCP or Azure HIPAA-eligible services, or Aptible), audit logging, SSO and a security review. The real product, but months of work and ongoing cost.

**Recommendation:** pilot with option 2, de-identified codes, and design so option 3 is possible later. Get a privacy lawyer's opinion before any real clinic uses it.

## Stay a research and wellness tool, not a medical device

Software that **diagnoses or recommends treatment** for a specific patient can count as a medical device (FDA "Software as a Medical Device"). Software that **records, organizes and displays** what a clinician chose to do generally isn't.

- Do: track sessions, show what happened, show published evidence, let clinicians draw conclusions.
- Avoid: "Play 110 BPM to treat this patient's freezing of gait", automated treatment recommendations, or anything claiming to diagnose.
- Keep the evidence browser as a literature tool, and keep language like "average change observed", not "this works".

## Product changes, in order

### Stage 1: ready for a few friendly therapists (about 1–2 months)

- **Accounts and auth.** Sign-in (an email link or passkeys) so each person sees only their own data.
- **Clients.** A therapist manages several clients (pseudonymous codes), each with their own studies.
- **Validated measures.** Beyond 1–10 mood and focus, offer standard scales. Check each one's license before including it.
  - Mood: PHQ-9 and GAD-7 (free to use). If PHQ-9 is included, item 9 asks about self-harm, so there must be a clear plan for what happens when someone answers it. That needs a clinician's input before shipping.
  - Affect: PANAS (short positive/negative affect).
  - Gait: gait speed (10-metre walk), cadence, Timed Up and Go.
  - Parkinson's: the MDS-UPDRS is licensed by the Movement Disorder Society, so check terms first.
- **Session protocol fields.** Tempo (BPM), instrument, active vs receptive, live vs recorded, and BPM relative to the client's cadence (e.g. "110%") for gait work.
- **Export.** CSV for every study; a printable PDF progress summary for clients or referrers.
- **Phone-friendly logging,** because sessions happen in a room, not at a desk.

### Stage 2: hosted pilot (about 2–4 months)

- Hosted deployment with backups, de-identified by design.
- **Better statistics for n-of-1:** randomization tests and confidence intervals instead of plain averages; handle missed sessions and carry-over between days.
- **Series of n-of-1:** run the same protocol across many clients and combine results (this is how n-of-1 trials turn into publishable evidence).
- **Link studies to evidence:** when designing a protocol, show the papers behind it (e.g. "rhythmic cueing at 100–110% cadence: 14 studies").
- **Consent tracking** for research use, and an audit log of who changed what.

### Stage 3: research-grade (6+ months)

- HIPAA-compliant hosting with BAAs, SSO for clinics, role-based access (therapist, supervisor, researcher).
- REDCap export and import (the standard in academic clinical research).
- IRB support: protocol templates and consent forms researchers can adapt for their ethics review.
- Gap finder (Phase 2 of the original roadmap): extract tempo, instrument and outcomes from abstracts and show what's under-studied.

## Validation before building

The cheapest way to avoid building the wrong thing is to talk to people first.

1. **Interview 5–8 music therapists.** Ask how they track progress today (paper? spreadsheets? EHR?), what they'd show a referrer or insurer, and what they'd never type into an app. The American Music Therapy Association (AMTA) and the Academy of Neurologic Music Therapy are good places to find them.
2. **Show them the current app** and the example studies. Watch where they get confused.
3. **Run one real pilot:** one therapist, 2–3 consenting clients, de-identified, 6 weeks.
4. **Run your own n-of-1 study now.** You'll find the rough edges in logging long before anyone else does, and it gives you a real story to tell.

## Ethics notes

- Personal n-of-1 use on yourself doesn't need ethics approval. Recruiting others, or publishing, generally does (IRB review).
- Mood tracking can surface people in crisis. Any version used by others needs visible crisis resources (the app already shows 988) and, for clinical use, a clear path for clinicians to follow up.
- Results from small n-of-1 studies are hypotheses, not proof. The UI should keep saying so.

## Open questions

- Who pays? Possible answers: therapists (low cost per seat), clinics, research grants (NIH and NSF fund music-and-health work), or it stays free and open source.
- Open source vs hosted: keep the core open (it builds trust with researchers) and offer hosting as the paid or supported option?
- How much of this should I build alone, and when do I bring in a clinician co-founder or advisor?

## Next three concrete steps

1. Run my own study in the app for 3 weeks, logging honestly.
2. Line up 3 music therapist conversations using the interview questions above.
3. Build Stage 1's first two items: accounts, and pseudonymous clients.
