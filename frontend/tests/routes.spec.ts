import { test, expect } from "@playwright/test";

const routes = [
  "/login",
  "/dashboard",
  "/network",
  "/vulnerabilities",
  "/web-security",
  "/threat-intel",
  "/ai-assistant",
  "/reports",
  "/settings",
];

for (const route of routes) {
  test(`${route} loads without runtime errors`, async ({ page }) => {
    const consoleErrors: string[] = [];

    page.on("console", (message) => {
      if (message.type() === "error") {
        consoleErrors.push(message.text());
      }
    });

    page.on("pageerror", (error) => {
      consoleErrors.push(error.message);
    });

    const response = await page.goto(route, {
      waitUntil: "networkidle",
    });

    expect(response?.status()).toBeLessThan(500);

    await expect(page.locator("body")).not.toBeEmpty();

    expect(consoleErrors).toEqual([]);
  });
}
