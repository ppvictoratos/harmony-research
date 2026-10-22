import axios from "axios";
import {
  SessionUpdate,
  StudyCreate,
  StudyDetail,
  StudyResults,
  StudySession,
  StudySummary,
} from "../types/Study";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/studies`,
});

export const studiesAPI = {
  list: () => api.get<StudySummary[]>(""),
  get: (id: number) => api.get<StudyDetail>(`/${id}`),
  create: (body: StudyCreate) => api.post<StudyDetail>("", body),
  remove: (id: number) => api.delete(`/${id}`),
  updateSession: (studyId: number, sessionId: number, body: SessionUpdate) =>
    api.patch<StudySession>(`/${studyId}/sessions/${sessionId}`, body),
  results: (id: number) => api.get<StudyResults>(`/${id}/results`),
};

export function errorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg).replace(/^Value error, /, "");
    if (!err.response) return "Couldn't reach the API. Is the backend running on http://localhost:8000?";
  }
  return fallback;
}
