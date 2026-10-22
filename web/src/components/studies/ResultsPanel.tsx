import { StudyResults } from "../../types/Study";

function signed(n: number): string {
  return `${n > 0 ? "+" : ""}${n.toFixed(1)}`;
}

/** Average mood change per condition, drawn as bars around zero with each session as a dot. */
export function ResultsPanel({ results }: { results: StudyResults }) {
  const rows = results.conditions;
  const allChanges = rows.flatMap((r) => r.mood_changes);
  const extent = Math.max(3, ...allChanges.map((c) => Math.abs(c)));
  const pos = (v: number) => 50 + (v / extent) * 50;

  const withData = rows.filter((r) => r.mood_change_avg != null);
  const best = withData.length
    ? withData.reduce((a, b) => ((b.mood_change_avg ?? 0) > (a.mood_change_avg ?? 0) ? b : a))
    : null;
  const minCompleted = rows.length ? Math.min(...rows.map((r) => r.completed)) : 0;

  return (
    <section className="card results-panel" aria-label="Results">
      <h2>Results so far</h2>
      {allChanges.length === 0 ? (
        <p className="muted">Complete a session to see how each condition changes your mood.</p>
      ) : (
        <>
          <p>
            {best && (best.mood_change_avg ?? 0) > 0 ? (
              <>
                So far, <strong>{best.condition}</strong> has the biggest average mood lift (
                {signed(best.mood_change_avg ?? 0)} points over {best.completed}{" "}
                {best.completed === 1 ? "session" : "sessions"}).
              </>
            ) : (
              <>No condition has lifted your mood on average yet.</>
            )}
          </p>
          <p className="muted small">
            {minCompleted < 5
              ? "Early days: with fewer than 5 sessions per condition, differences are mostly noise. Keep going."
              : "Differences of less than a point are within normal day-to-day variation."}
          </p>

          <div className="effect-chart" role="img" aria-label="Average mood change per condition">
            <div className="effect-axis">
              <span>{signed(-extent)}</span>
              <span>0</span>
              <span>{signed(extent)}</span>
            </div>
            {rows.map((r) => {
              const avg = r.mood_change_avg;
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
                    {r.mood_changes.map((c, i) => (
                      <span key={i} className="effect-dot" style={{ left: `${pos(c)}%` }} title={`${signed(c)}`} />
                    ))}
                  </div>
                  <div className="effect-value">{avg != null ? signed(avg) : "—"}</div>
                </div>
              );
            })}
          </div>
          <p className="muted small">Bars show the average change in mood (after minus before). Dots are single sessions.</p>
        </>
      )}
    </section>
  );
}
