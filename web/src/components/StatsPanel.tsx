import { StatsResponse } from "../types/Evidence";

interface StatsPanelProps {
  stats: StatsResponse;
  onYearClick?: (year: number) => void;
}

export function StatsPanel({ stats, onYearClick }: StatsPanelProps) {
  const years = Object.entries(stats.by_year)
    .filter(([y]) => y !== "unknown")
    .map(([y, n]) => [Number(y), n] as const)
    .sort((a, b) => a[0] - b[0]);
  const max = Math.max(1, ...years.map(([, n]) => n));
  const first = years[0]?.[0];
  const last = years[years.length - 1]?.[0];

  return (
    <section className="stats" aria-label="Evidence overview">
      <div className="tiles">
        <div className="tile">
          <span className="value">{stats.total_studies.toLocaleString()}</span>
          <span className="label">studies</span>
        </div>
        <div className="tile">
          <span className="value">{(stats.by_source.pubmed ?? 0).toLocaleString()}</span>
          <span className="label">PubMed papers</span>
        </div>
        <div className="tile">
          <span className="value">{(stats.by_source.clinicaltrials ?? 0).toLocaleString()}</span>
          <span className="label">clinical trials</span>
        </div>
      </div>
      {years.length > 0 && (
        <figure className="years">
          <figcaption>Studies per year · click a bar to filter</figcaption>
          <div className="bars">
            {years.map(([year, n]) => (
              <button
                key={year}
                type="button"
                className="bar"
                style={{ height: `${Math.max(4, (n / max) * 100)}%` }}
                title={`${year}: ${n} ${n === 1 ? "study" : "studies"}`}
                aria-label={`${year}: ${n} studies`}
                onClick={() => onYearClick?.(year)}
              />
            ))}
          </div>
          <div className="axis">
            <span>{first}</span>
            <span>{last}</span>
          </div>
        </figure>
      )}
    </section>
  );
}
