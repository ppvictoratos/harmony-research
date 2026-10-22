import { expect, test, type Page } from "@playwright/test";

async function openNewStudyForm(page: Page) {
  await page.goto("/#/studies");
  const newStudy = page.getByRole("button", { name: "+ New study" });
  const form = page.getByRole("heading", { name: "Design a new study" });
  // An empty database opens the form straight away; otherwise click "New study"
  await expect(newStudy.or(form)).toBeVisible();
  if (await newStudy.isVisible()) await newStudy.click();
  await expect(form).toBeVisible();
}

async function createStudy(page: Page, name: string) {
  await openNewStudyForm(page);
  await page.getByLabel("Name").fill(name);
  await page.getByLabel("Your question").fill("Which lifts my mood more?");
  await page.getByRole("button", { name: "Guitar", exact: true }).click();
  await page.getByRole("button", { name: "Endel", exact: true }).click();
  await page.getByLabel("Sessions per condition").fill("2");
  await expect(page.getByText("That's 4 daily sessions")).toBeVisible();
  await page.getByRole("button", { name: "Create study & schedule" }).click();
  await expect(page).toHaveURL(/#\/studies\/\d+$/);
  await expect(page.getByRole("heading", { name })).toBeVisible();
}

const uniqueName = (label: string) => `${label} ${Date.now()}-${Math.floor(Math.random() * 1e6)}`;

test("design a study, log a session and see results", async ({ page }) => {
  const name = uniqueName("E2E guitar vs Endel");
  await createStudy(page, name);
  await expect(page.getByText(/0 of 4 sessions done/)).toBeVisible();
  await expect(page.getByLabel("Schedule").locator(".schedule-item")).toHaveCount(4);

  const complete = page.getByRole("button", { name: "Complete session" });
  await expect(complete).toBeDisabled();
  await page.getByRole("button", { name: "Mood before: 4" }).click();
  await expect(complete).toBeDisabled();
  await page.getByRole("button", { name: "Mood after: 7" }).click();
  await page.getByLabel("Notes (optional)").fill("Felt great");
  await complete.click();

  await expect(page.getByText(/1 of 4 sessions done/)).toBeVisible();
  await expect(page.getByText(/biggest average mood lift \(\+3\.0 points over 1 session\)/)).toBeVisible();
  await expect(page.getByLabel("Schedule").locator(".schedule-item.done")).toContainText("+3");
  // The logger moves on to session 2
  await expect(page.getByText(/^Session 2 ·/)).toBeVisible();
});

test("edit a completed session from the schedule", async ({ page }) => {
  await createStudy(page, uniqueName("E2E edit"));
  await page.getByRole("button", { name: "Mood before: 5" }).click();
  await page.getByRole("button", { name: "Mood after: 6" }).click();
  await page.getByRole("button", { name: "Complete session" }).click();
  await expect(page.getByText(/1 of 4 sessions done/)).toBeVisible();

  await page.getByLabel("Schedule").locator(".schedule-item.done").click();
  await page.getByRole("button", { name: "Mood after: 9" }).click();
  await page.getByRole("button", { name: "Save changes" }).click();
  await expect(page.getByLabel("Schedule").locator(".schedule-item.done")).toContainText("+4");
});

test("rejects duplicate condition names", async ({ page }) => {
  await openNewStudyForm(page);
  await page.getByLabel("Name").fill(uniqueName("E2E duplicate"));
  await page.getByLabel("Condition 1").fill("Piano");
  await page.getByLabel("Condition 2").fill("piano");
  await page.getByRole("button", { name: "Create study & schedule" }).click();
  await expect(page.getByRole("alert")).toContainText("condition names must be different");
});

test("delete a study", async ({ page }) => {
  const name = uniqueName("E2E delete");
  await createStudy(page, name);
  page.once("dialog", (dialog) => dialog.accept());
  await page.getByRole("button", { name: "Delete study" }).click();
  await expect(page).toHaveURL(/#\/studies$/);
  await expect(page.getByRole("button", { name: "+ New study" }).or(page.getByRole("heading", { name: "Design a new study" }))).toBeVisible();
  await expect(page.getByText(name)).toHaveCount(0);
});

test("unknown study shows an error", async ({ page }) => {
  await page.goto("/#/studies/999999");
  await expect(page.getByRole("alert")).toContainText("Study not found");
});
