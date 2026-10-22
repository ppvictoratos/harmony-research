import { useState } from "react";
import { errorMessage, studiesAPI } from "../../services/studies";
import { StudyDetail } from "../../types/Study";

interface NewStudyFormProps {
  onCreated: (study: StudyDetail) => void;
  onCancel: () => void;
}

const SUGGESTIONS = ["Guitar", "Piano", "Singing", "Drums", "Endel", "Lo-fi playlist", "Silence"];

function todayISO(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export function NewStudyForm({ onCreated, onCancel }: NewStudyFormProps) {
  const [title, setTitle] = useState("");
  const [question, setQuestion] = useState("");
  const [conditions, setConditions] = useState<string[]>(["", ""]);
  const [minutes, setMinutes] = useState(20);
  const [perCondition, setPerCondition] = useState(7);
  const [startDate, setStartDate] = useState(todayISO());
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const filled = conditions.map((c) => c.trim()).filter(Boolean);
  const totalDays = Math.max(filled.length, 2) * perCondition;

  const setCondition = (i: number, value: string) =>
    setConditions(conditions.map((c, j) => (j === i ? value : c)));

  const addSuggestion = (name: string) => {
    if (filled.some((c) => c.toLowerCase() === name.toLowerCase())) return;
    const empty = conditions.findIndex((c) => !c.trim());
    if (empty >= 0) setCondition(empty, name);
    else if (conditions.length < 6) setConditions([...conditions, name]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const resp = await studiesAPI.create({
        title: title.trim(),
        question: question.trim() || undefined,
        conditions: filled,
        session_minutes: minutes,
        sessions_per_condition: perCondition,
        start_date: startDate || undefined,
      });
      onCreated(resp.data);
    } catch (err) {
      setError(errorMessage(err, "Couldn't create the study."));
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="card study-form" onSubmit={handleSubmit}>
      <h2>Design a new study</h2>
      <p className="muted">
        An n-of-1 study compares a few conditions on one person: you. Each day you get one condition, in a
        shuffled but balanced order, and rate how you feel before and after.
      </p>

      <label className="field">
        <span>Name</span>
        <input
          required
          maxLength={200}
          value={title}
          placeholder="e.g. Guitar vs Endel for low mornings"
          onChange={(e) => setTitle(e.target.value)}
        />
      </label>

      <label className="field">
        <span>Your question</span>
        <input
          value={question}
          placeholder="e.g. Which lifts my mood more: playing guitar or listening to Endel?"
          onChange={(e) => setQuestion(e.target.value)}
        />
      </label>

      <fieldset className="field">
        <legend>Conditions to compare (2–6)</legend>
        <div className="conditions">
          {conditions.map((c, i) => (
            <div className="condition-row" key={i}>
              <input
                aria-label={`Condition ${i + 1}`}
                maxLength={100}
                value={c}
                placeholder={i === 0 ? "e.g. Guitar" : i === 1 ? "e.g. Silence (a good baseline)" : "Condition"}
                onChange={(e) => setCondition(i, e.target.value)}
              />
              {conditions.length > 2 && (
                <button
                  type="button"
                  className="link"
                  aria-label={`Remove condition ${i + 1}`}
                  onClick={() => setConditions(conditions.filter((_, j) => j !== i))}
                >
                  Remove
                </button>
              )}
            </div>
          ))}
        </div>
        <div className="chips">
          {conditions.length < 6 && (
            <button type="button" className="chip" onClick={() => setConditions([...conditions, ""])}>
              + Add condition
            </button>
          )}
          {SUGGESTIONS.map((s) => (
            <button key={s} type="button" className="chip" onClick={() => addSuggestion(s)}>
              {s}
            </button>
          ))}
        </div>
      </fieldset>

      <div className="field-row">
        <label className="field">
          <span>Minutes per session</span>
          <input type="number" min={1} max={240} value={minutes} onChange={(e) => setMinutes(Number(e.target.value))} />
        </label>
        <label className="field">
          <span>Sessions per condition</span>
          <input
            type="number"
            min={2}
            max={30}
            value={perCondition}
            onChange={(e) => setPerCondition(Number(e.target.value))}
          />
        </label>
        <label className="field">
          <span>Start date</span>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </label>
      </div>

      <p className="muted">
        That's {totalDays} daily sessions, about {Math.ceil(totalDays / 7)} weeks. More sessions per condition make
        the results more trustworthy; 7 or more is a good start.
      </p>

      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}

      <div className="actions">
        <button type="submit" className="primary" disabled={saving || filled.length < 2 || !title.trim()}>
          {saving ? "Creating…" : "Create study & schedule"}
        </button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}
