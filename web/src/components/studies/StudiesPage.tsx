import { useEffect, useState } from "react";
import { errorMessage, studiesAPI } from "../../services/studies";
import { StudySummary } from "../../types/Study";
import { NewStudyForm } from "./NewStudyForm";
import { WellbeingNote } from "./WellbeingNote";

export function StudiesPage() {
  const [studies, setStudies] = useState<StudySummary[] | null>(null);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    studiesAPI
      .list()
      .then((resp) => {
        setStudies(resp.data);
        if (resp.data.length === 0) setCreating(true);
      })
      .catch((err) => setError(errorMessage(err, "Couldn't load your studies.")));
  }, []);

  if (error) {
    return (
      <div className="error" role="alert">
        {error}
      </div>
    );
  }

  if (!studies) {
    return <div className="empty">Loading…</div>;
  }

  return (
    <>
      {creating ? (
        <NewStudyForm
          onCreated={(study) => {
            window.location.hash = `#/studies/${study.id}`;
          }}
          onCancel={() => setCreating(false)}
        />
      ) : (
        <div className="section-head">
          <h2>My studies</h2>
          <button type="button" className="primary" onClick={() => setCreating(true)}>
            + New study
          </button>
        </div>
      )}

      {studies.length > 0 && (
        <ul className="study-list">
          {studies.map((s) => {
            const pct = s.total_sessions ? Math.round((s.completed_sessions / s.total_sessions) * 100) : 0;
            return (
              <li key={s.id}>
                <a className="card study-card" href={`#/studies/${s.id}`}>
                  <span className="study-title">{s.title}</span>
                  {s.question && <span className="muted">{s.question}</span>}
                  <span className="muted small">{s.conditions.join(" · ")}</span>
                  <span className="progress" aria-label={`${pct}% complete`}>
                    <span style={{ width: `${pct}%` }} />
                  </span>
                  <span className="muted small">
                    {s.completed_sessions} of {s.total_sessions} sessions done
                  </span>
                </a>
              </li>
            );
          })}
        </ul>
      )}

      <WellbeingNote />
    </>
  );
}
