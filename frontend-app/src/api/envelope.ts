/**
 * The standard response envelope shared by every backend endpoint
 * (see ticket #27 and the `patterns` steering).
 *
 * - `success` — whether the request succeeded.
 * - `data` — the payload, `null` on error.
 * - `error` — a user-friendly message, `null` on success.
 * - `meta` — pagination metadata, present only on paginated collections.
 */
export interface ApiEnvelope<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  meta?: PaginationMeta;
}

export interface PaginationMeta {
  total: number;
  page: number;
  limit: number;
}
