import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { EvidenceTable } from "../src/components/EvidenceTable";
import { EvidenceListResponse } from "../src/types/Evidence";

const data: EvidenceListResponse = {
  total: 45,
  page: 1,
  page_size: 20,
  results: [
    {
      id: 1,
      study_id: "pubmed_1",
      title: "Rhythmic auditory cueing and gait",
      authors: "Smith J.",
      year: 2020,
      abstract: "Metronome at 110% of cadence.",
      source: "pubmed",
      url: "https://pubmed.ncbi.nlm.nih.gov/1/",
      date_added: "2026-10-21T00:00:00",
    },
    {
      id: 2,
      study_id: "clinicaltrials_NCT1",
      title: "Music therapy trial",
      year: null,
      sample_size: 40,
      outcomes: "Gait Speed|UPDRS III",
      source: "clinicaltrials",
      date_added: "2026-10-21T00:00:00",
    },
  ],
};

describe("EvidenceTable", () => {
  it("renders rows, counts and pages", () => {
    render(<EvidenceTable data={data} isLoading={false} onPageChange={() => {}} />);
    expect(screen.getByText("45 results")).toBeInTheDocument();
    expect(screen.getByText("Page 1 of 3")).toBeInTheDocument();
    expect(screen.getByText("Trial")).toBeInTheDocument();
    expect(screen.getByText("—", { selector: ".col-year" })).toBeInTheDocument();
  });

  it("expands a row to show the abstract and details", async () => {
    render(<EvidenceTable data={data} isLoading={false} onPageChange={() => {}} />);
    expect(screen.queryByText("Metronome at 110% of cadence.")).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Rhythmic auditory cueing and gait" }));
    expect(screen.getByText("Metronome at 110% of cadence.")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Open on PubMed/ })).toHaveAttribute("href", data.results[0].url);

    await userEvent.click(screen.getByRole("button", { name: "Music therapy trial" }));
    expect(screen.getByText("Gait Speed · UPDRS III")).toBeInTheDocument();
    expect(screen.getByText("40")).toBeInTheDocument();
  });

  it("disables Previous on the first page and pages forward", async () => {
    const onPageChange = vi.fn();
    render(<EvidenceTable data={data} isLoading={false} onPageChange={onPageChange} />);
    expect(screen.getByRole("button", { name: /Previous/ })).toBeDisabled();
    await userEvent.click(screen.getByRole("button", { name: /Next/ }));
    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it("shows an empty state", () => {
    render(
      <EvidenceTable data={{ ...data, total: 0, results: [] }} isLoading={false} onPageChange={() => {}} />,
    );
    expect(screen.getByText(/No evidence found/)).toBeInTheDocument();
  });
});
