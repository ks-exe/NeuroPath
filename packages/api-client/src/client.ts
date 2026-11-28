import type { ApiErrorBody, HealthResponse } from "./types";

/**
 * The only URL prefix this client may call. The Web_App talks to the API
 * exclusively under /api/v1 and never to AWS services (R2.8).
 */
export const API_PREFIX = "/api/v1";

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly fields: Record<string, string> | null;
  readonly requestId: string | null;
  /** Seconds from the Retry-After header (429), when present. */
  readonly retryAfterSeconds: number | null;

  constructor(status: number, body: ApiErrorBody, retryAfterSeconds: number | null = null) {
    super(body.message);
    this.name = "ApiError";
    this.status = status;
    this.code = body.code;
    this.fields = body.fields;
    this.requestId = body.request_id;
    this.retryAfterSeconds = retryAfterSeconds;
  }
}

/**
 * Normalizes the envelope `fields` value. The API sends a list of
 * `{field, message}`; a plain map is accepted too. Returns null when empty.
 */
export function normalizeFieldErrors(value: unknown): Record<string, string> | null {
  const out: Record<string, string> = {};
  if (Array.isArray(value)) {
    for (const item of value) {
      if (
        typeof item === "object" &&
        item !== null &&
        typeof (item as { field?: unknown }).field === "string" &&
        typeof (item as { message?: unknown }).message === "string"
      ) {
        const field = (item as { field: string }).field.replace(/^body\./, "");
        if (!(field in out)) out[field] = (item as { message: string }).message;
      }
    }
  } else if (typeof value === "object" && value !== null) {
    for (const [k, v] of Object.entries(value)) {
      if (typeof v === "string") out[k] = v;
    }
  }
  return Object.keys(out).length > 0 ? out : null;
}

/** Parses Retry-After as delta-seconds or an HTTP date. */
export function parseRetryAfter(header: string | null, now: number = Date.now()): number | null {
  if (header === null || header.trim() === "") return null;
  const trimmed = header.trim();
  if (/^\d+$/.test(trimmed)) return Number(trimmed);
  const date = Date.parse(trimmed);
  if (Number.isNaN(date)) return null;
  return Math.max(0, Math.ceil((date - now) / 1000));
}

export interface ApiClientOptions {
  /**
   * Origin to prepend (server-side rendering only, e.g. "http://api:8000").
   * Browsers use same-origin relative URLs. Must not carry a path.
   */
  origin?: string;
  fetchImpl?: typeof fetch;
  /** Extra headers, e.g. a forwarded session cookie on the server. */
  headers?: Record<string, string>;
}

/** Builds a request path, rejecting anything that would leave /api/v1. */
export function buildApiPath(path: string): string {
  if (!path.startsWith("/") || path.startsWith("//")) {
    throw new Error("API path must start with a single '/'");
  }
  if (/^\/[a-z][a-z0-9+.-]*:/i.test(path) || path.includes("\\")) {
    throw new Error("API path must be relative");
  }
  const pathOnly = path.split(/[?#]/, 1)[0] ?? "";
  if (pathOnly.split("/").some((s) => s === ".." || s === "." )) {
    throw new Error("API path must not contain dot segments");
  }
  return `${API_PREFIX}${path}`;
}

function isErrorBody(value: unknown): value is ApiErrorBody {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as ApiErrorBody).code === "string" &&
    typeof (value as ApiErrorBody).message === "string"
  );
}

export class ApiClient {
  private readonly origin: string;
  private readonly fetchImpl: typeof fetch;
  private readonly headers: Record<string, string>;

  constructor(options: ApiClientOptions = {}) {
    const origin = (options.origin ?? "").replace(/\/+$/, "");
    if (origin !== "") {
      const url = new URL(origin);
      if (url.pathname !== "/" || url.search !== "" || url.hash !== "") {
        throw new Error("origin must not include a path, query, or fragment");
      }
    }
    this.origin = origin;
    this.fetchImpl = options.fetchImpl ?? ((...args) => fetch(...args));
    this.headers = options.headers ?? {};
  }

  async request<T>(
    method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE",
    path: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${this.origin}${buildApiPath(path)}`;
    const headers: Record<string, string> = {
      Accept: "application/json",
      ...this.headers,
    };
    const init: RequestInit = { method, headers, credentials: "include" };
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(body);
    }
    const response = await this.fetchImpl(url, init);
    const text = await response.text();
    let parsed: unknown = undefined;
    if (text !== "") {
      try {
        parsed = JSON.parse(text);
      } catch {
        parsed = undefined;
      }
    }
    if (!response.ok) {
      const errBody: ApiErrorBody = isErrorBody(parsed)
        ? {
            code: parsed.code,
            message: parsed.message,
            fields: normalizeFieldErrors(parsed.fields),
            request_id: parsed.request_id ?? null,
          }
        : {
            code: "unexpected_error",
            message: `Request failed with status ${response.status}`,
            fields: null,
            request_id: null,
          };
      throw new ApiError(response.status, errBody, parseRetryAfter(response.headers.get("Retry-After")));
    }
    return parsed as T;
  }

  get<T>(path: string): Promise<T> {
    return this.request<T>("GET", path);
  }

  post<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>("POST", path, body);
  }

  health(): Promise<HealthResponse> {
    return this.get<HealthResponse>("/health");
  }
}
