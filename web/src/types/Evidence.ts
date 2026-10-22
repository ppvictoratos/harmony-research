export interface Evidence {
  id: number;
  study_id: string;
  title: string;
  authors?: string | null;
  year?: number | null;
  abstract?: string | null;
  intervention_type?: string | null;
  outcomes?: string | null;
  sample_size?: number | null;
  effect_size?: number | null;
  source: string;
  url?: string | null;
  date_added: string;
}

export interface EvidenceListResponse {
  total: number;
  page: number;
  page_size: number;
  results: Evidence[];
}

export interface StatsResponse {
  total_studies: number;
  by_source: Record<string, number>;
  by_year: Record<string, number>;
  by_intervention: Record<string, number>;
}

export interface Filters {
  source?: string;
  year_from?: number;
  year_to?: number;
}
