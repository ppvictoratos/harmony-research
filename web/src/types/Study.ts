export interface StudySession {
  id: number;
  session_number: number;
  condition: string;
  planned_date: string; // YYYY-MM-DD
  completed_at: string | null;
  mood_before: number | null;
  mood_after: number | null;
  focus_before: number | null;
  focus_after: number | null;
  notes: string | null;
}

export interface StudySummary {
  id: number;
  title: string;
  question: string | null;
  conditions: string[];
  session_minutes: number;
  created_at: string;
  total_sessions: number;
  completed_sessions: number;
}

export interface StudyDetail extends StudySummary {
  sessions: StudySession[];
}

export interface StudyCreate {
  title: string;
  question?: string;
  conditions: string[];
  session_minutes: number;
  sessions_per_condition: number;
  start_date?: string;
}

export interface SessionUpdate {
  mood_before?: number | null;
  mood_after?: number | null;
  focus_before?: number | null;
  focus_after?: number | null;
  notes?: string | null;
  completed?: boolean;
}

export interface ConditionResult {
  condition: string;
  planned: number;
  completed: number;
  mood_before_avg: number | null;
  mood_after_avg: number | null;
  mood_change_avg: number | null;
  mood_changes: number[];
  focus_change_avg: number | null;
  focus_changes: number[];
}

export interface StudyResults {
  study_id: number;
  completed_sessions: number;
  total_sessions: number;
  conditions: ConditionResult[];
}
