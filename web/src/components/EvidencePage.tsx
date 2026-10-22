import { useEffect, useRef, useState } from "react";
import { evidenceAPI } from "../services/api";
import { EvidenceListResponse, Filters, StatsResponse } from "../types/Evidence";
import { EvidenceTable } from "./EvidenceTable";
import { FilterPanel } from "./FilterPanel";
import { SearchForm } from "./SearchForm";
import { StatsPanel } from "./StatsPanel";

export function EvidencePage() {
  const [data, setData] = useState<EvidenceListResponse | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<Filters>({});
  const [page, setPage] = useState(1);
  const requestId = useRef(0);

  useEffect(() => {
    evidenceAPI
      .stats()
      .then((resp) => setStats(resp.data))
      .catch((err) => console.error("Failed to load stats:", err));
  }, []);

  useEffect(() => {
    // Ignore responses from older requests that finish late
    const id = ++requestId.current;
    setIsLoading(true);
    const request = searchQuery
      ? evidenceAPI.search(searchQuery, page, 20, filters)
      : evidenceAPI.list(page, 20, filters);
    request
      .then((resp) => {
        if (id !== requestId.current) return;
        setData(resp.data);
        setError(null);
      })
      .catch((err) => {
        if (id !== requestId.current) return;
        console.error("Failed to load evidence:", err);
        setError("Couldn't reach the API. Is the backend running on http://localhost:8000?");
      })
      .finally(() => {
        if (id === requestId.current) setIsLoading(false);
      });
  }, [searchQuery, filters, page]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setPage(1);
  };

  const handleFilters = (next: Filters) => {
    setFilters(next);
    setPage(1);
  };

  return (
    <>
      {stats && (
        <StatsPanel
          stats={stats}
          onYearClick={(year) => handleFilters({ ...filters, year_from: year, year_to: year })}
        />
      )}

      <SearchForm onSearch={handleSearch} />
      <FilterPanel filters={filters} onChange={handleFilters} />

      {error ? (
        <div className="error" role="alert">
          {error}
        </div>
      ) : (
        <EvidenceTable
          data={data}
          isLoading={isLoading}
          onPageChange={(p) => {
            setPage(p);
            window.scrollTo({ top: 0, behavior: "smooth" });
          }}
        />
      )}
    </>
  );
}
