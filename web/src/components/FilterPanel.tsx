import { Filters } from "../types/Evidence";

interface FilterPanelProps {
  filters: Filters;
  onChange: (filters: Filters) => void;
}

const SOURCES = [
  { value: "", label: "All sources" },
  { value: "pubmed", label: "PubMed papers" },
  { value: "clinicaltrials", label: "Clinical trials" },
];

function toYear(value: string): number | undefined {
  const n = parseInt(value, 10);
  return Number.isNaN(n) ? undefined : n;
}

export function FilterPanel({ filters, onChange }: FilterPanelProps) {
  const hasFilters = Boolean(filters.source || filters.year_from || filters.year_to);

  return (
    <div className="filters" aria-label="Filters">
      <div className="segmented" role="group" aria-label="Source">
        {SOURCES.map((s) => (
          <button
            key={s.value}
            type="button"
            aria-pressed={(filters.source || "") === s.value}
            onClick={() => onChange({ ...filters, source: s.value || undefined })}
          >
            {s.label}
          </button>
        ))}
      </div>
      <label>
        From
        <input
          type="number"
          inputMode="numeric"
          aria-label="Year from"
          placeholder="1979"
          value={filters.year_from ?? ""}
          onChange={(e) => onChange({ ...filters, year_from: toYear(e.target.value) })}
        />
      </label>
      <label>
        To
        <input
          type="number"
          inputMode="numeric"
          aria-label="Year to"
          placeholder="2026"
          value={filters.year_to ?? ""}
          onChange={(e) => onChange({ ...filters, year_to: toYear(e.target.value) })}
        />
      </label>
      {hasFilters && (
        <button type="button" className="link" onClick={() => onChange({})}>
          Reset filters
        </button>
      )}
    </div>
  );
}
