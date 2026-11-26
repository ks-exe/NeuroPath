/** Structured error envelope returned by every failing API call (R19.2, R19.3). */
export interface ApiErrorBody {
  code: string;
  message: string;
  fields: Record<string, string> | null;
  request_id: string | null;
}

/** Response of GET /api/v1/health. */
export interface HealthResponse {
  status: string;
}
