import axios from "axios";
import { EvidenceListResponse, Filters, StatsResponse } from "../types/Evidence";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

export const evidenceAPI = {
  list: (page: number = 1, pageSize: number = 20, filters: Filters = {}) =>
    api.get<EvidenceListResponse>("/evidence", {
      params: { page, page_size: pageSize, ...filters },
    }),

  search: (query: string, page: number = 1, pageSize: number = 20, filters: Filters = {}) =>
    api.get<EvidenceListResponse>("/evidence/search", {
      params: { q: query, page, page_size: pageSize, ...filters },
    }),

  stats: () => api.get<StatsResponse>("/evidence/stats"),
};
