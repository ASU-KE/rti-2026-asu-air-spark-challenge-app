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
  it("renders semantic landmarks", () => {
    renderApp();
    expect(screen.getByRole("banner")).toBeInTheDocument();
    expect(screen.getByRole("navigation")).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("exposes primary navigation to all four screens", () => {
    renderApp();
    const nav = screen.getByRole("navigation", { name: /primary/i });
    for (const label of [
      "Experiment Builder",
      "Network Overview",
      "Run Monitor",
      "Dataset Manager",
    ]) {
      expect(
        within(nav).getByRole("link", { name: label }),
      ).toBeInTheDocument();
    }
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

    await user.click(screen.getByRole("link", { name: "Run Monitor" }));

    expect(
      screen.getByRole("heading", { level: 1, name: /run monitor/i }),
    ).toBeInTheDocument();
  });
});
