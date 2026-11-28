/** One field-level error as sent by the API envelope. */
export interface ApiFieldError {
  field: string;
  message: string;
}

/**
 * Structured error envelope returned by every failing API call (R19.2, R19.3).
 * The API sends `fields` as a list of `{field, message}`; the client normalizes
 * it to a map keyed by field name (first message per field wins).
 */
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

/** Response of POST /api/v1/public/inquiries/submission-token. */
export interface SubmissionTokenResponse {
  submission_token: string;
}

/** Body of POST /api/v1/public/inquiries (R14.1, R14.10). Extra keys are rejected. */
export interface InquiryRequest {
  submission_token: string;
  name: string;
  email: string;
  company?: string;
  title: string;
  problem_description: string;
  desired_outcome?: string;
  existing_systems?: string;
  data_and_integrations?: string;
  expected_users?: string;
  constraints?: string;
  budget_range?: string;
  preferred_timeline?: string;
  service_hint?: string;
  consent_contact: boolean;
  consent_ai_processing: boolean;
  consent_wording_version: string;
  /** Honeypot (R14.8); always empty for humans. */
  website: string;
}

/** Receipt of an accepted inquiry; carries no personal data. */
export interface InquiryReceipt {
  project_inquiry_id: string;
  project_id: string;
  status_label: string;
}
