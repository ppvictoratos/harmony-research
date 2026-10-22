import { defineConfig, devices } from "@playwright/test";

// End-to-end tests run the real API against a throwaway Postgres database
// (<DATABASE_URL name>_e2e, wiped and re-seeded on every run) on separate ports,
// so they never touch your data and can run alongside `dev.sh`.
const API_PORT = 8001;
const WEB_PORT = 3100;

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: `http://localhost:${WEB_PORT}`,
    trace: "retain-on-failure",
    // Use the installed Google Chrome instead of downloading Playwright's browsers
    channel: "chrome",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], channel: "chrome" } },
    { name: "mobile", use: { ...devices["Pixel 7"], channel: "chrome" } },
  ],
  webServer: [
    {
      command: `cd ../backend && PYTHONPATH=. ./venv/bin/python scripts/e2e_server.py --port ${API_PORT} --web-origin http://localhost:${WEB_PORT}`,
      url: `http://127.0.0.1:${API_PORT}/health`,
      reuseExistingServer: false,
      timeout: 60_000,
    },
    {
      command: `VITE_API_BASE_URL=http://127.0.0.1:${API_PORT} ./node_modules/.bin/vite --port ${WEB_PORT} --strictPort`,
      url: `http://localhost:${WEB_PORT}`,
      reuseExistingServer: false,
      timeout: 60_000,
    },
  ],
});
