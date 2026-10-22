import { useState } from "react";
import { ConditionResult, StudyResults } from "../../types/Study";

type Measure = "mood" | "focus";

const pick = (r: ConditionResult, m: Measure) =>
  m === "mood"
    ? { avg: r.mood_change_avg, changes: r.mood_changes }
    : { avg: r.focus_change_avg, changes: r.focus_changes };

function signed(n: number): string {
  return `${n > 0 ? "+" : ""}${n.toFixed(1)}`;
}

/** Average change per condition, drawn as bars around zero with each session as a dot. */
export function ResultsPanel({ results }: { results: StudyResults }) {
  const rows = results.conditions;
  const hasFocus = rows.some((r) => r.focus_changes.length > 0);
  const [chosen, setMeasure] = useState<Measure>("mood");
  const measure: Measure = hasFocus ? chosen : "mood";
  const allChanges = rows.flatMap((r) => pick(r, measure).changes);
  const extent = Math.max(3, ...allChanges.map((c) => Math.abs(c)));
  const pos = (v: number) => 50 + (v / extent) * 50;

  const withData = rows.filter((r) => pick(r, measure).avg != null);
  const best = withData.length
    ? withData.reduce((a, b) => ((pick(b, measure).avg ?? 0) > (pick(a, measure).avg ?? 0) ? b : a))
    : null;
  const bestAvg = best ? pick(best, measure).avg ?? 0 : 0;
  const bestCount = best ? pick(best, measure).changes.length : 0;
  const minCompleted = rows.length ? Math.min(...rows.map((r) => r.completed)) : 0;

  return (
    <section className="card results-panel" aria-label="Results">
      <div className="section-head">
        <h2>Results so far</h2>
        {hasFocus && (
          <div className="segmented" role="group" aria-label="Measure">
            {(["mood", "focus"] as const).map((m) => (
              <button key={m} type="button" aria-pressed={measure === m} onClick={() => setMeasure(m)}>
                {m === "mood" ? "Mood" : "Focus"}
              </button>
            ))}
          </div>
        )}
      </div>
      {allChanges.length === 0 ? (
        <p className="muted">Complete a session to see how each condition changes your {measure}.</p>
      ) : (
        <>
          <p>
            {best && bestAvg > 0 ? (
              <>
                So far, <strong>{best.condition}</strong> has the biggest average {measure} lift (
                {signed(bestAvg)} points over {bestCount} {bestCount === 1 ? "session" : "sessions"}).
              </>
            ) : (
              <>No condition has lifted your {measure} on average yet.</>
            )}
          </p>
          <p className="muted small">
            {minCompleted < 5
              ? "Early days: with fewer than 5 sessions per condition, differences are mostly noise. Keep going."
              : "Differences of less than a point are within normal day-to-day variation."}
          </p>

          <div className="effect-chart" role="img" aria-label={`Average ${measure} change per condition`}>
            <div className="effect-axis">
              <span>{signed(-extent)}</span>
              <span>0</span>
              <span>{signed(extent)}</span>
            </div>
            {rows.map((r) => {
              const { avg, changes } = pick(r, measure);
              return (
                <div className="effect-row" key={r.condition}>
                  <div className="effect-label">
                    <span>{r.condition}</span>
                    <span className="muted small">
                      {r.completed}/{r.planned} done
                    </span>
                  </div>
                  <div className="effect-track">
                    <span className="effect-zero" />
                    {avg != null && (
                      <span
                        className={`effect-bar ${avg < 0 ? "neg" : "pos"}`}
                        style={{
                          left: `${Math.min(50, pos(avg))}%`,
                          width: `${Math.abs(pos(avg) - 50)}%`,
                        }}
                      />
                    )}
                    {changes.map((c, i) => (
                      <span key={i} className="effect-dot" style={{ left: `${pos(c)}%` }} title={`${signed(c)}`} />
                    ))}
                  </div>
                  <div className="effect-value">{avg != null ? signed(avg) : "—"}</div>
                </div>
              );
            })}
          </div>
          <p className="muted small">Bars show the average change in {measure} (after minus before). Dots are single sessions.</p>
        </>
      )}
    </section>
  );
}
