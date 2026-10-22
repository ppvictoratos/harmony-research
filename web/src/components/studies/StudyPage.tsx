import { useCallback, useEffect, useMemo, useState } from "react";
import { errorMessage, studiesAPI } from "../../services/studies";
import { StudyDetail, StudyResults, StudySession } from "../../types/Study";
import { ResultsPanel } from "./ResultsPanel";
import { SessionLogger } from "./SessionLogger";
import { WellbeingNote } from "./WellbeingNote";

function shortDate(iso: string): string {
  return new Date(`${iso}T00:00:00`).toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export function StudyPage({ studyId }: { studyId: number }) {
  const [study, setStudy] = useState<StudyDetail | null>(null);
  const [results, setResults] = useState<StudyResults | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const [s, r] = await Promise.all([studiesAPI.get(studyId), studiesAPI.results(studyId)]);
      setStudy(s.data);
      setResults(r.data);
      setError(null);
    } catch (err) {
      setError(errorMessage(err, "Couldn't load this study."));
    }
  }, [studyId]);

  useEffect(() => {
    load();
  }, [load]);

  const nextSession = useMemo(() => study?.sessions.find((s) => !s.completed_at) ?? null, [study]);
  const selected = study?.sessions.find((s) => s.id === selectedId) ?? nextSession;

  const handleSaved = async (saved: StudySession) => {
    setSelectedId(saved.completed_at ? null : saved.id);
    await load();
  };

  const handleDelete = async () => {
    if (!study || !window.confirm(`Delete "${study.title}" and all its sessions? This can't be undone.`)) return;
    try {
      await studiesAPI.remove(study.id);
      window.location.hash = "#/studies";
    } catch (err) {
      setError(errorMessage(err, "Couldn't delete this study."));
    }
  };

  if (error) {
    return (
      <div className="error" role="alert">
        {error}
      </div>
    );
  }
  if (!study || !results) {
    return <div className="empty">Loading…</div>;
  }

  const pct = Math.round((study.completed_sessions / study.total_sessions) * 100);

  return (
    <>
      <a className="back" href="#/studies">
        ← All studies
      </a>
      <div className="study-head">
        <h2>{study.title}</h2>
        {study.question && <p className="question">{study.question}</p>}
        <div className="progress" aria-label={`${pct}% complete`}>
          <span style={{ width: `${pct}%` }} />
        </div>
        <p className="muted small">
          {study.completed_sessions} of {study.total_sessions} sessions done · {study.session_minutes} min each ·
          comparing {study.conditions.join(", ")}
        </p>
      </div>

      {selected ? (
        <SessionLogger studyId={study.id} session={selected} minutes={study.session_minutes} onSaved={handleSaved} />
      ) : (
        <div className="card done">
          <h2>Study complete 🎉</h2>
          <p className="muted">Every session is logged. Your results are below.</p>
        </div>
      )}

      <ResultsPanel results={results} />

      <section className="card" aria-label="Schedule">
        <h2>Schedule</h2>
        <p className="muted small">Click any session to log or edit it.</p>
        <ol className="schedule">
          {study.sessions.map((s) => {
            const change =
              s.mood_before != null && s.mood_after != null ? s.mood_after - s.mood_before : null;
            const isSelected = selected?.id === s.id;
            return (
              <li key={s.id}>
                <button
                  type="button"
                  className={`schedule-item${s.completed_at ? " done" : ""}${isSelected ? " selected" : ""}`}
                  aria-current={isSelected ? "true" : undefined}
                  onClick={() => setSelectedId(s.id)}
                >
                  <span className="num">{s.session_number}</span>
                  <span className="date">{shortDate(s.planned_date)}</span>
                  <span className="cond">{s.condition}</span>
                  <span className="status">
                    {s.completed_at ? (change != null ? `${change > 0 ? "+" : ""}${change}` : "✓") : "—"}
                  </span>
                </button>
              </li>
            );
          })}
        </ol>
      </section>

      <div className="danger-zone">
        <button type="button" className="link danger" onClick={handleDelete}>
          Delete study
        </button>
      </div>

      <WellbeingNote />
    </>
  );
}
