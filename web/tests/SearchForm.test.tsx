import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { SearchForm } from "../src/components/SearchForm";

describe("SearchForm", () => {
  it("submits the trimmed query", async () => {
    const onSearch = vi.fn();
    render(<SearchForm onSearch={onSearch} />);
    await userEvent.type(screen.getByLabelText("Search evidence"), "  metronome  {enter}");
    expect(onSearch).toHaveBeenCalledWith("metronome");
  });

  it("clears the query and resets results", async () => {
    const onSearch = vi.fn();
    render(<SearchForm onSearch={onSearch} />);
    await userEvent.type(screen.getByLabelText("Search evidence"), "singing");
    await userEvent.click(screen.getByRole("button", { name: "Clear" }));
    expect(screen.getByLabelText("Search evidence")).toHaveValue("");
    expect(onSearch).toHaveBeenLastCalledWith("");
  });
});
