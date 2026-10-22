import { expect, test } from "@playwright/test";

test("dark by default, toggle to light, and remember it", async ({ page }) => {
  await page.goto("/");
  const html = page.locator("html");
  await expect(html).toHaveAttribute("data-theme", "dark");

  await page.getByRole("button", { name: "Toggle light and dark theme" }).click();
  await expect(html).toHaveAttribute("data-theme", "light");
  await expect(page.locator("body")).toHaveCSS("background-color", "rgb(241, 235, 225)");

  await page.reload();
  await expect(html).toHaveAttribute("data-theme", "light");
});

test("tabs switch between evidence and studies", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: "My studies" }).click();
  await expect(page).toHaveURL(/#\/studies$/);
  await expect(page.getByRole("link", { name: "My studies" })).toHaveAttribute("aria-current", "page");
  await page.getByRole("link", { name: "Evidence" }).click();
  await expect(page.getByLabel("Search evidence")).toBeVisible();
});
