import type { ApiEnvelope } from "./envelope";

/**
 * Base URL for the backend API. In local dev, Vite proxies `/api` to the
 * FastAPI backend (see `vite.config.ts`); in other environments it can be
 * overridden with `VITE_API_BASE_URL`.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

/** Raised when the backend returns a non-2xx response or an error envelope. */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Thin typed fetch wrapper around the standard response envelope. It unwraps
 * `data` on success and throws {@link ApiError} on failure, so callers work
 * with the payload directly. Screen slices build their resource calls on top
 * of this base.
 */
export async function apiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });

  let envelope: ApiEnvelope<T> | null = null;
  try {
    envelope = (await response.json()) as ApiEnvelope<T>;
  } catch {
    // Non-JSON body — fall through to a status-based error below.
  }

  if (!response.ok || !envelope?.success) {
    const message =
      envelope?.error ?? `Request to ${path} failed (${response.status})`;
    throw new ApiError(message, response.status);
  }

  return envelope.data as T;
}
