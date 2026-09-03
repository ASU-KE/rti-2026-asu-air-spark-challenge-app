import { describe, expect, it } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { AppRoutes } from "./routes";

function renderApp(initialPath = "/") {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <AppRoutes />
    </MemoryRouter>,
  );
}

describe("App shell", () => {
  it("renders the ASU Unity banner and a main landmark", () => {
    renderApp();
    expect(screen.getByRole("banner")).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("exposes site navigation to all four screens", () => {
    renderApp();
    const siteNav = screen.getByRole("navigation", { name: /site/i });
    for (const label of [
      "Experiment Builder",
      "Network Overview",
      "Run Monitor",
      "Dataset Manager",
    ]) {
      expect(
        within(siteNav).getByRole("link", { name: label }),
      ).toBeInTheDocument();
    }
  });

  it("provides a skip link that targets the main landmark", () => {
    renderApp();
    const skipLink = screen.getByRole("link", {
      name: /skip to main content/i,
    });
    const target = skipLink.getAttribute("href")?.replace(/^#/, "");

    expect(target).toBeTruthy();
    // The skip link must resolve to the main region, not a dangling fragment.
    expect(document.getElementById(target as string)).toBe(
      screen.getByRole("main"),
    );
  });

  it("lands on the Experiment Builder screen by default", () => {
    renderApp();
    expect(
      screen.getByRole("heading", { level: 1, name: /experiment builder/i }),
    ).toBeInTheDocument();
  });

  it("navigates to another screen when its nav link is activated", async () => {
    const user = userEvent.setup();
    renderApp();

    const siteNav = screen.getByRole("navigation", { name: /site/i });
    await user.click(within(siteNav).getByRole("link", { name: "Run Monitor" }));

    expect(
      screen.getByRole("heading", { level: 1, name: /run monitor/i }),
    ).toBeInTheDocument();
  });

  it("renders the deep-linked screen on a direct visit", () => {
    renderApp("/datasets");
    expect(
      screen.getByRole("heading", { level: 1, name: /dataset manager/i }),
    ).toBeInTheDocument();
  });
});
