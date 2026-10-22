import { useState } from "react";

interface SearchFormProps {
  onSearch: (query: string) => void;
  initialQuery?: string;
}

export function SearchForm({ onSearch, initialQuery = "" }: SearchFormProps) {
  const [query, setQuery] = useState(initialQuery);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query.trim());
  };

  const handleClear = () => {
    setQuery("");
    onSearch("");
  };

  return (
    <form className="search" onSubmit={handleSubmit} role="search">
      <input
        type="search"
        aria-label="Search evidence"
        placeholder="Search titles, authors, abstracts, outcomes…  e.g. metronome, singing, freezing"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit" className="primary">
        Search
      </button>
      {query && (
        <button type="button" onClick={handleClear}>
          Clear
        </button>
      )}
    </form>
  );
}
