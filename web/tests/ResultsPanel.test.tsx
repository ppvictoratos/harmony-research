import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ResultsPanel } from "../src/components/studies/ResultsPanel";
import { StudyResults } from "../src/types/Study";

const base = (overrides: Partial<StudyResults["conditions"][number]>) => ({
  condition: "X",
  planned: 7,
  completed: 0,
  mood_before_avg: null,
  mood_after_avg: null,
  mood_change_avg: null,
  mood_changes: [],
  focus_change_avg: null,
  focus_changes: [],
  ...overrides,
});

describe("ResultsPanel", () => {
  it("prompts to log when nothing is completed", () => {
    render(<ResultsPanel results={{ study_id: 1, completed_sessions: 0, total_sessions: 14, conditions: [base({})] }} />);
    expect(screen.getByText(/Complete a session/)).toBeInTheDocument();
  });

  it("names the condition with the biggest lift and warns about small samples", () => {
    render(
      <ResultsPanel
        results={{
          study_id: 1,
          completed_sessions: 3,
          total_sessions: 14,
          conditions: [
            base({ condition: "Guitar", completed: 2, mood_change_avg: 2, mood_changes: [3, 1] }),
            base({ condition: "Silence", completed: 1, mood_change_avg: -1, mood_changes: [-1] }),
          ],
        }}
      />,
    );
    expect(screen.getByText("Guitar", { selector: "strong" })).toBeInTheDocument();
    expect(screen.getByText(/\+2\.0 points over 2 sessions/)).toBeInTheDocument();
    expect(screen.getByText(/Early days/)).toBeInTheDocument();
    expect(screen.getByText("-1.0")).toBeInTheDocument();
  });
});
