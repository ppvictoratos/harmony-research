import { expect, test } from "@playwright/test";

// Fixtures come from backend/scripts/e2e_server.py: 3 PubMed papers, 1 trial, 1 preprint.

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("5 results")).toBeVisible();
});

test("shows overview stats", async ({ page }) => {
  const stats = page.getByLabel("Evidence overview");
  await expect(stats.getByText("studies", { exact: true })).toBeVisible();
  await expect(stats.locator(".tile").filter({ hasText: "papers" })).toContainText("3");
  await expect(stats.locator(".tile").filter({ hasText: "clinical trials" })).toContainText("1");
  await expect(stats.locator(".tile").filter({ hasText: "preprints" })).toContainText("1");
});

test("search matches abstracts", async ({ page }) => {
  await page.getByLabel("Search evidence").fill("metronome");
  await page.getByLabel("Search evidence").press("Enter");
  await expect(page.getByText("1 result", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: /Rhythmic auditory cueing improves gait speed/ })).toBeVisible();
});

test("shows an empty state and clears back to everything", async ({ page }) => {
  await page.getByLabel("Search evidence").fill("zzzz-no-match");
  await page.getByRole("button", { name: "Search", exact: true }).click();
  await expect(page.getByText(/No evidence found/)).toBeVisible();
  await page.getByRole("button", { name: "Clear" }).click();
  await expect(page.getByText("5 results")).toBeVisible();
});

test("filters by source", async ({ page }) => {
  await page.getByRole("button", { name: "Preprints" }).click();
  await expect(page.getByText("1 result", { exact: true })).toBeVisible();
  await expect(page.locator(".badge")).toHaveText(["Preprint"]);

  await page.getByRole("button", { name: "Reset filters" }).click();
  await expect(page.getByText("5 results")).toBeVisible();
});

test("filters by year range", async ({ page }) => {
  await page.getByLabel("Year from").fill("2024");
  await page.getByLabel("Year to").fill("2025");
  await expect(page.getByText("2 results")).toBeVisible();
});

test("opens a trial to show its details", async ({ page }) => {
  await page.getByRole("button", { name: "Music therapy for freezing of gait" }).click();
  await expect(page.getByText("Participants walk to music matched to their cadence.")).toBeVisible();
  await expect(page.getByText("Freezing of Gait Questionnaire · Gait speed")).toBeVisible();
  await expect(page.getByRole("link", { name: /Open on ClinicalTrials\.gov/ })).toHaveAttribute(
    "href",
    "https://clinicaltrials.gov/study/NCTE2E1",
  );
});

test("marks preprints as not peer reviewed", async ({ page }) => {
  await page.getByRole("button", { name: /Walking to the beat with drumming/ }).click();
  await expect(page.getByText("Preprint: not yet peer reviewed.")).toBeVisible();
});

test("never scrolls sideways", async ({ page }) => {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(0);
});
