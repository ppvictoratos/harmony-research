import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { RatingInput } from "../src/components/studies/RatingInput";

describe("RatingInput", () => {
  it("selects and clears a value", async () => {
    const onChange = vi.fn();
    const { rerender } = render(<RatingInput label="Mood before" value={null} onChange={onChange} />);
    await userEvent.click(screen.getByRole("button", { name: "Mood before: 7" }));
    expect(onChange).toHaveBeenLastCalledWith(7);

    rerender(<RatingInput label="Mood before" value={7} onChange={onChange} />);
    expect(screen.getByRole("button", { name: "Mood before: 7" })).toHaveAttribute("aria-pressed", "true");
    await userEvent.click(screen.getByRole("button", { name: "Mood before: 7" }));
    expect(onChange).toHaveBeenLastCalledWith(null);
  });
});
