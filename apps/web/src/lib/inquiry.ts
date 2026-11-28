import type { InquiryRequest } from "@neuropath/api-client";
import type { ServiceGroupId } from "@content";

/**
 * Client-side rules for the project inquiry form (R14.1, R14.4). They mirror
 * the API rules in apps/api (schemas/inquiries.py, services/inquiries.py);
 * the API stays authoritative.
 */

// COPY FOR FOUNDER REVIEW: consent wording needs legal review before launch (A-11).
// Bump CONSENT_WORDING_VERSION whenever either consent text changes (R14.10).
export const CONSENT_WORDING_VERSION = "2025-01";
export const CONSENT_CONTACT_TEXT =
  "I agree that NEUROPATH may store the information in this form and contact me about my inquiry.";
export const CONSENT_AI_TEXT =
  "Optional: I agree that NEUROPATH may use AI-assisted tools to analyze the content of my inquiry.";

export const SHORT_MAX = 200;
export const LONG_MAX = 5000;
export const PROBLEM_MIN = 20;

// Same syntactic rule as the API (R14.3).
const EMAIL_RE = /^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$/;

export const SERVICE_HINT_IDS: readonly ServiceGroupId[] = ["A", "B", "C", "D", "E", "F"];

/** Returns the hint only when it is one of the group ids A to F (R12.11). */
export function parseServiceHint(value: unknown): ServiceGroupId | "" {
  const raw = Array.isArray(value) ? value[0] : value;
  if (typeof raw !== "string") return "";
  const upper = raw.trim().toUpperCase();
  return (SERVICE_HINT_IDS as readonly string[]).includes(upper) ? (upper as ServiceGroupId) : "";
}

export type TextFieldName =
  | "name"
  | "email"
  | "company"
  | "title"
  | "problem_description"
  | "desired_outcome"
  | "existing_systems"
  | "data_and_integrations"
  | "expected_users"
  | "constraints"
  | "budget_range"
  | "preferred_timeline"
  | "service_hint";

export interface InquiryValues extends Record<TextFieldName, string> {
  consent_contact: boolean;
  consent_ai_processing: boolean;
}

export type InquiryFieldName = TextFieldName | "consent_contact" | "consent_ai_processing";
export type InquiryErrors = Partial<Record<InquiryFieldName, string>>;

export const SHORT_FIELDS: readonly TextFieldName[] = [
  "name",
  "email",
  "company",
  "title",
  "budget_range",
  "preferred_timeline",
  "service_hint",
];
export const LONG_FIELDS: readonly TextFieldName[] = [
  "problem_description",
  "desired_outcome",
  "existing_systems",
  "data_and_integrations",
  "expected_users",
  "constraints",
];

/** Display and focus order of the form controls. */
export const FIELD_ORDER: readonly InquiryFieldName[] = [
  "name",
  "email",
  "company",
  "title",
  "service_hint",
  "problem_description",
  "desired_outcome",
  "existing_systems",
  "data_and_integrations",
  "expected_users",
  "constraints",
  "budget_range",
  "preferred_timeline",
  "consent_contact",
  "consent_ai_processing",
];

export function emptyInquiry(serviceHint: ServiceGroupId | "" = ""): InquiryValues {
  return {
    name: "",
    email: "",
    company: "",
    title: "",
    problem_description: "",
    desired_outcome: "",
    existing_systems: "",
    data_and_integrations: "",
    expected_users: "",
    constraints: "",
    budget_range: "",
    preferred_timeline: "",
    service_hint: serviceHint,
    consent_contact: false,
    consent_ai_processing: false,
  };
}

export function validateInquiry(values: InquiryValues): InquiryErrors {
  const errors: InquiryErrors = {};
  const required: readonly TextFieldName[] = ["name", "email", "title", "problem_description"];
  for (const name of required) {
    if (values[name].trim() === "") errors[name] = "This field is required.";
  }
  const email = values.email.trim();
  if (!errors.email && !EMAIL_RE.test(email)) {
    errors.email = "Enter a valid email address, for example name@example.com.";
  }
  const problem = values.problem_description.trim();
  if (!errors.problem_description && problem.length < PROBLEM_MIN) {
    errors.problem_description = `Describe the problem in at least ${PROBLEM_MIN} characters.`;
  }
  for (const name of SHORT_FIELDS) {
    if (!errors[name] && values[name].trim().length > SHORT_MAX) {
      errors[name] = `Use at most ${SHORT_MAX} characters.`;
    }
  }
  for (const name of LONG_FIELDS) {
    if (!errors[name] && values[name].trim().length > LONG_MAX) {
      errors[name] = `Use at most ${LONG_MAX} characters.`;
    }
  }
  if (!values.consent_contact) {
    errors.consent_contact = "Consent is required to send the inquiry.";
  }
  return errors;
}

/** First invalid field in display order, used for focus on submit. */
export function firstInvalidField(errors: InquiryErrors): InquiryFieldName | undefined {
  return FIELD_ORDER.find((name) => errors[name] !== undefined);
}

/** Builds the request body; optional empty fields are omitted. */
export function toInquiryRequest(values: InquiryValues, submissionToken: string, honeypot: string): InquiryRequest {
  const body: InquiryRequest = {
    submission_token: submissionToken,
    name: values.name.trim(),
    email: values.email.trim(),
    title: values.title.trim(),
    problem_description: values.problem_description.trim(),
    consent_contact: values.consent_contact,
    consent_ai_processing: values.consent_ai_processing,
    consent_wording_version: CONSENT_WORDING_VERSION,
    website: honeypot,
  };
  const optional = [
    "company",
    "desired_outcome",
    "existing_systems",
    "data_and_integrations",
    "expected_users",
    "constraints",
    "budget_range",
    "preferred_timeline",
    "service_hint",
  ] as const;
  for (const name of optional) {
    const v = values[name].trim();
    if (v !== "") body[name] = v;
  }
  return body;
}

/** Maps server field errors onto known form fields; unknown keys are dropped. */
export function mapServerFieldErrors(fields: Record<string, string> | null): InquiryErrors {
  const errors: InquiryErrors = {};
  if (!fields) return errors;
  for (const [key, message] of Object.entries(fields)) {
    if ((FIELD_ORDER as readonly string[]).includes(key)) errors[key as InquiryFieldName] = message;
  }
  return errors;
}

/** "try again in N minutes" text from Retry-After seconds (R14.7). */
export function retryMessage(seconds: number | null): string {
  if (seconds === null || seconds <= 0) return "Too many submissions. Please try again in a few minutes.";
  const minutes = Math.max(1, Math.ceil(seconds / 60));
  return `Too many submissions. Please try again in ${minutes} minute${minutes === 1 ? "" : "s"}.`;
}
