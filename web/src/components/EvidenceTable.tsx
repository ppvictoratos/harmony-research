import { Fragment, useState } from "react";
import { Evidence, EvidenceListResponse } from "../types/Evidence";

interface EvidenceTableProps {
  data: EvidenceListResponse | null;
  isLoading: boolean;
  onPageChange: (page: number) => void;
}

const SOURCE_LABEL: Record<string, string> = {
  pubmed: "PubMed",
  clinicaltrials: "Trial",
};

function Details({ ev }: { ev: Evidence }) {
  return (
    <div className="details">
      {ev.abstract ? (
        <p className="abstract">{ev.abstract}</p>
      ) : (
        <p className="muted">No abstract available.</p>
      )}
      <dl>
        {ev.sample_size != null && (
          <>
            <dt>Participants</dt>
            <dd>{ev.sample_size}</dd>
          </>
        )}
        {ev.intervention_type && (
          <>
            <dt>Intervention</dt>
            <dd>{ev.intervention_type.split("|").join(", ")}</dd>
          </>
        )}
        {ev.outcomes && (
          <>
            <dt>Primary outcomes</dt>
            <dd>{ev.outcomes.split("|").join(" · ")}</dd>
          </>
        )}
      </dl>
      {ev.url && (
        <a href={ev.url} target="_blank" rel="noopener noreferrer">
          Open on {ev.source === "pubmed" ? "PubMed" : "ClinicalTrials.gov"} ↗
        </a>
      )}
    </div>
  );
}

export function EvidenceTable({ data, isLoading, onPageChange }: EvidenceTableProps) {
  const [expanded, setExpanded] = useState<number | null>(null);

  if (!data && isLoading) {
    return <div className="empty">Loading…</div>;
  }

  if (!data || data.results.length === 0) {
    return <div className="empty">No evidence found. Try a different search or reset the filters.</div>;
  }

  const totalPages = Math.max(1, Math.ceil(data.total / data.page_size));

  return (
    <div className={isLoading ? "results loading" : "results"}>
      <p className="count">
        {data.total.toLocaleString()} {data.total === 1 ? "result" : "results"}
      </p>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th className="col-authors">Authors</th>
            <th className="col-year">Year</th>
            <th className="col-source">Source</th>
          </tr>
        </thead>
        <tbody>
          {data.results.map((ev) => {
            const open = expanded === ev.id;
            return (
              <Fragment key={ev.id}>
                <tr className={open ? "row open" : "row"}>
                  <td>
                    <button
                      type="button"
                      className="title"
                      aria-expanded={open}
                      onClick={() => setExpanded(open ? null : ev.id)}
                    >
                      {ev.title}
                    </button>
                  </td>
                  <td className="col-authors">{ev.authors || "—"}</td>
                  <td className="col-year">{ev.year ?? "—"}</td>
                  <td className="col-source">
                    <span className={`badge ${ev.source}`}>{SOURCE_LABEL[ev.source] ?? ev.source}</span>
                  </td>
                </tr>
                {open && (
                  <tr className="detail-row">
                    <td colSpan={4}>
                      <Details ev={ev} />
                    </td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>

      <nav className="pager" aria-label="Pagination">
        <button onClick={() => onPageChange(data.page - 1)} disabled={data.page <= 1}>
          ← Previous
        </button>
        <span>
          Page {data.page} of {totalPages}
        </span>
        <button onClick={() => onPageChange(data.page + 1)} disabled={data.page >= totalPages}>
          Next →
        </button>
      </nav>
    </div>
  );
}
