import { useEffect, useState } from "react";
import { errorMessage, studiesAPI } from "../../services/studies";
import { StudySession } from "../../types/Study";
import { RatingInput } from "./RatingInput";

interface SessionLoggerProps {
  studyId: number;
  session: StudySession;
  minutes: number;
  onSaved: (session: StudySession) => void;
}

export function SessionLogger({ studyId, session, minutes, onSaved }: SessionLoggerProps) {
  const [moodBefore, setMoodBefore] = useState(session.mood_before);
  const [moodAfter, setMoodAfter] = useState(session.mood_after);
  const [focusBefore, setFocusBefore] = useState(session.focus_before);
  const [focusAfter, setFocusAfter] = useState(session.focus_after);
  const [notes, setNotes] = useState(session.notes ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setMoodBefore(session.mood_before);
    setMoodAfter(session.mood_after);
    setFocusBefore(session.focus_before);
    setFocusAfter(session.focus_after);
    setNotes(session.notes ?? "");
    setError(null);
  }, [session]);

  const save = async (complete: boolean) => {
    setSaving(true);
    setError(null);
    try {
      const resp = await studiesAPI.updateSession(studyId, session.id, {
        mood_before: moodBefore,
        mood_after: moodAfter,
        focus_before: focusBefore,
        focus_after: focusAfter,
        notes: notes.trim() || null,
        ...(complete ? { completed: true } : {}),
      });
      onSaved(resp.data);
    } catch (err) {
      setError(errorMessage(err, "Couldn't save this session."));
    } finally {
      setSaving(false);
    }
  };

  const done = Boolean(session.completed_at);
  const date = new Date(`${session.planned_date}T00:00:00`).toLocaleDateString(undefined, {
    weekday: "long",
    month: "short",
    day: "numeric",
  });

  return (
    <section className="card logger" aria-label="Log a session">
      <p className="eyebrow">
        Session {session.session_number} · {date}
        {done && " · completed"}
      </p>
      <h2>
        {session.condition} <span className="muted">for {minutes} min</span>
      </h2>

      <div className="logger-grid">
        <div>
          <h3>Before</h3>
          <RatingInput label="Mood before" value={moodBefore} onChange={setMoodBefore} />
          <RatingInput label="Focus before (optional)" value={focusBefore} onChange={setFocusBefore} />
        </div>
        <div>
          <h3>After</h3>
          <RatingInput label="Mood after" value={moodAfter} onChange={setMoodAfter} />
          <RatingInput label="Focus after (optional)" value={focusAfter} onChange={setFocusAfter} />
        </div>
      </div>

      <label className="field">
        <span>Notes (optional)</span>
        <textarea
          rows={2}
          value={notes}
          placeholder="What did you play or hear? Anything unusual today (sleep, stress, caffeine)?"
          onChange={(e) => setNotes(e.target.value)}
        />
      </label>

      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}

      <div className="actions">
        {done ? (
          <button type="button" className="primary" disabled={saving} onClick={() => save(false)}>
            {saving ? "Saving…" : "Save changes"}
          </button>
        ) : (
          <>
            <button
              type="button"
              className="primary"
              disabled={saving || moodBefore == null || moodAfter == null}
              onClick={() => save(true)}
            >
              {saving ? "Saving…" : "Complete session"}
            </button>
            <button type="button" disabled={saving} onClick={() => save(false)}>
              Save for later
            </button>
          </>
        )}
      </div>
    </section>
  );
}
