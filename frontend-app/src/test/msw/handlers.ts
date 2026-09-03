import { http, HttpResponse } from "msw";

/**
 * Default MSW handlers shared across the suite.
 *
 * The scaffold ships a single handler for the backend health check so that
 * screen slices have a working baseline to extend. Per-test handlers can be
 * layered on with `server.use(...)`.
 */
export const handlers = [
  http.get("/api/health", () =>
    HttpResponse.json({
      success: true,
      data: { status: "ok" },
      error: null,
    }),
  ),
];
