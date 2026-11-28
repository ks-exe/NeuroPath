"use client";

import * as React from "react";
import { ApiError, type InquiryReceipt, type SubmissionTokenResponse } from "@neuropath/api-client";
import { Button, Field, TextareaField, cn } from "@neuropath/ui";
import type { ServiceGroupId } from "@content";
import { api } from "@/lib/api";
import {
  CONSENT_AI_TEXT,
  CONSENT_CONTACT_TEXT,
  LONG_MAX,
  SHORT_MAX,
  emptyInquiry,
  firstInvalidField,
  mapServerFieldErrors,
  retryMessage,
  toInquiryRequest,
  validateInquiry,
  type InquiryErrors,
  type InquiryFieldName,
  type InquiryValues,
  type TextFieldName,
} from "@/lib/inquiry";

export interface ServiceHintOption {
  id: ServiceGroupId;
  name: string;
}

interface InquiryFormProps {
  /** Prefilled optional hint from `?serviceHint=` (R12.11); never required. */
  initialServiceHint: ServiceGroupId | "";
  serviceOptions: readonly ServiceHintOption[];
}

type TokenState = { status: "loading" } | { status: "ready"; token: string } | { status: "error" };

const fieldId = (name: InquiryFieldName) => `inquiry-${name}`;

const checkboxClass =
  "mt-0.5 h-5 w-5 shrink-0 rounded border border-input accent-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2";

// Visually hidden but present in the DOM for bots (R14.8).
const honeypotWrapper = "absolute -left-[10000px] top-auto h-px w-px overflow-hidden";

export function InquiryForm({ initialServiceHint, serviceOptions }: InquiryFormProps) {
  const [values, setValues] = React.useState<InquiryValues>(() => emptyInquiry(initialServiceHint));
  const [errors, setErrors] = React.useState<InquiryErrors>({});
  const [token, setToken] = React.useState<TokenState>({ status: "loading" });
  const [pending, setPending] = React.useState(false);
  const [formError, setFormError] = React.useState<string | null>(null);
  const [announcement, setAnnouncement] = React.useState("");
  const [receipt, setReceipt] = React.useState<InquiryReceipt | null>(null);
  const [honeypot, setHoneypot] = React.useState("");
  const [focusTarget, setFocusTarget] = React.useState<InquiryFieldName | null>(null);
  const confirmationRef = React.useRef<HTMLDivElement>(null);

  const loadToken = React.useCallback(async () => {
    setToken({ status: "loading" });
    try {
      const res = await api.post<SubmissionTokenResponse>("/public/inquiries/submission-token");
      setToken({ status: "ready", token: res.submission_token });
    } catch {
      setToken({ status: "error" });
    }
  }, []);

  React.useEffect(() => {
    void loadToken();
  }, [loadToken]);

  React.useEffect(() => {
    if (receipt) confirmationRef.current?.focus();
  }, [receipt]);

  React.useEffect(() => {
    if (focusTarget && !pending) {
      document.getElementById(fieldId(focusTarget))?.focus();
      setFocusTarget(null);
    }
  }, [focusTarget, pending]);

  function setText(name: TextFieldName) {
    return (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const value = event.target.value;
      setValues((prev) => ({ ...prev, [name]: value }));
      if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
    };
  }

  function setChecked(name: "consent_contact" | "consent_ai_processing") {
    return (event: React.ChangeEvent<HTMLInputElement>) => {
      const checked = event.target.checked;
      setValues((prev) => ({ ...prev, [name]: checked }));
      if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
    };
  }

  function showFieldErrors(next: InquiryErrors) {
    setErrors(next);
    const first = firstInvalidField(next);
    const count = Object.values(next).filter(Boolean).length;
    setAnnouncement(
      `The form has ${count} error${count === 1 ? "" : "s"}. Please correct the highlighted field${count === 1 ? "" : "s"}.`,
    );
    // Focus after the next render, once controls are no longer disabled.
    if (first) setFocusTarget(first);
  }

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (pending) return;
    setFormError(null);
    setReceipt(null);

    const clientErrors = validateInquiry(values);
    if (Object.keys(clientErrors).length > 0) {
      showFieldErrors(clientErrors);
      return;
    }
    if (token.status !== "ready") {
      const msg = "The form is not ready yet. Please wait a moment or reload the form.";
      setFormError(msg);
      setAnnouncement(msg);
      return;
    }

    setErrors({});
    setPending(true);
    setAnnouncement("Sending your inquiry.");
    try {
      // The same token is reused for retries of this submission (R14.14).
      const res = await api.post<InquiryReceipt>("/public/inquiries", toInquiryRequest(values, token.token, honeypot));
      setReceipt(res);
      setValues(emptyInquiry(""));
      setHoneypot("");
      setAnnouncement("Your inquiry was sent.");
      void loadToken();
    } catch (err) {
      // Values are kept on every failure (R14.5).
      if (err instanceof ApiError && err.status === 429) {
        const msg = retryMessage(err.retryAfterSeconds);
        setFormError(msg);
        setAnnouncement(msg);
      } else if (err instanceof ApiError && err.status === 422) {
        const mapped = mapServerFieldErrors(err.fields);
        if (Object.keys(mapped).length > 0) {
          showFieldErrors(mapped);
        } else {
          const msg = `The inquiry could not be accepted. ${err.message}`;
          setFormError(msg);
          setAnnouncement(msg);
        }
      } else {
        const ref = err instanceof ApiError && err.requestId ? ` Reference: ${err.requestId}.` : "";
        const msg = `Something went wrong and the inquiry was not sent. Please try again.${ref}`;
        setFormError(msg);
        setAnnouncement(msg);
      }
    } finally {
      setPending(false);
    }
  }

  const textProps = (name: TextFieldName) => ({
    id: fieldId(name),
    name,
    value: values[name],
    onChange: setText(name),
    error: errors[name],
    disabled: pending,
  });

  const hintError = errors.service_hint;

  return (
    <div className="flex flex-col gap-6">
      {/* Live region for status and error summaries (R15.8). */}
      <div aria-live="polite" role="status" className="sr-only">
        {announcement}
      </div>

      {receipt ? (
        <div
          ref={confirmationRef}
          tabIndex={-1}
          className="rounded border border-border bg-secondary p-4 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <p className="font-body text-base font-medium text-foreground">Thank you. Your inquiry was received.</p>
          <p className="mt-1 font-body text-sm text-muted-foreground">
            Status: {receipt.status_label}. NEUROPATH will review it and respond.
          </p>
        </div>
      ) : null}

      {token.status === "error" ? (
        <div className="flex flex-col items-start gap-2 rounded border-2 border-foreground p-4" role="alert">
          <p className="font-body text-sm text-foreground">The form could not be prepared. Check your connection and try again.</p>
          <Button variant="outline" size="sm" onClick={() => void loadToken()}>
            Try again
          </Button>
        </div>
      ) : null}

      {formError ? (
        <div className="rounded border-2 border-foreground p-4" role="alert">
          <p className="font-body text-sm text-foreground">{formError}</p>
        </div>
      ) : null}

      <form noValidate onSubmit={onSubmit} aria-busy={pending} className="relative flex flex-col gap-5">
        <p className="font-body text-sm text-muted-foreground">
          Fields marked <span aria-hidden="true">*</span>
          <span className="sr-only">with an asterisk</span> are required.
        </p>

        <div className="grid gap-5 md:grid-cols-2">
          <Field label="Name" required autoComplete="name" maxLength={SHORT_MAX} {...textProps("name")} />
          <Field label="Email" type="email" required autoComplete="email" maxLength={SHORT_MAX} {...textProps("email")} />
          <Field label="Company or organization" autoComplete="organization" maxLength={SHORT_MAX} {...textProps("company")} />
          <Field label="Project title" required maxLength={SHORT_MAX} {...textProps("title")} />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor={fieldId("service_hint")} className="text-sm font-medium text-foreground">
            Service area (optional)
          </label>
          <p id={`${fieldId("service_hint")}-hint`} className="text-sm text-muted-foreground">
            You do not need to choose a technology. Leave this empty if you are not sure.
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <select
              id={fieldId("service_hint")}
              name="service_hint"
              value={values.service_hint}
              onChange={setText("service_hint")}
              disabled={pending}
              aria-invalid={hintError ? true : undefined}
              aria-describedby={[`${fieldId("service_hint")}-hint`, hintError ? `${fieldId("service_hint")}-error` : null]
                .filter(Boolean)
                .join(" ")}
              className={cn(
                "h-10 min-w-0 flex-1 rounded border border-input bg-background px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50",
                hintError && "border-2 border-foreground",
              )}
            >
              <option value="">No preference</option>
              {serviceOptions.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.name}
                </option>
              ))}
            </select>
            {values.service_hint !== "" ? (
              <Button
                variant="ghost"
                size="sm"
                disabled={pending}
                onClick={() => setValues((prev) => ({ ...prev, service_hint: "" }))}
              >
                Clear service area
              </Button>
            ) : null}
          </div>
          <p id={`${fieldId("service_hint")}-error`} role="alert" className="text-sm font-medium text-foreground">
            {hintError ? <span className="font-mono">Error: </span> : null}
            {hintError}
          </p>
        </div>

        <TextareaField
          label="Problem description"
          required
          rows={6}
          hint="Describe the problem you want to solve, in at least 20 characters."
          maxLength={LONG_MAX}
          {...textProps("problem_description")}
        />
        <TextareaField label="Desired outcome" maxLength={LONG_MAX} {...textProps("desired_outcome")} />
        <TextareaField label="Existing systems" maxLength={LONG_MAX} {...textProps("existing_systems")} />
        <TextareaField label="Relevant data or integrations" maxLength={LONG_MAX} {...textProps("data_and_integrations")} />
        <TextareaField label="Expected users" rows={3} maxLength={LONG_MAX} {...textProps("expected_users")} />
        <TextareaField label="Additional constraints" rows={3} maxLength={LONG_MAX} {...textProps("constraints")} />

        <div className="grid gap-5 md:grid-cols-2">
          <Field label="Budget range (optional)" maxLength={SHORT_MAX} {...textProps("budget_range")} />
          <Field label="Preferred timeline (optional)" maxLength={SHORT_MAX} {...textProps("preferred_timeline")} />
        </div>

        <fieldset className="flex flex-col gap-4">
          <legend className="mb-2 text-sm font-medium text-foreground">Consent</legend>
          <div className="flex flex-col gap-1.5">
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                id={fieldId("consent_contact")}
                name="consent_contact"
                checked={values.consent_contact}
                onChange={setChecked("consent_contact")}
                disabled={pending}
                required
                aria-invalid={errors.consent_contact ? true : undefined}
                aria-describedby={errors.consent_contact ? `${fieldId("consent_contact")}-error` : undefined}
                className={checkboxClass}
              />
              <label htmlFor={fieldId("consent_contact")} className="font-body text-sm text-foreground">
                {CONSENT_CONTACT_TEXT}
                <span aria-hidden="true"> *</span>
              </label>
            </div>
            <p id={`${fieldId("consent_contact")}-error`} role="alert" className="text-sm font-medium text-foreground">
              {errors.consent_contact ? <span className="font-mono">Error: </span> : null}
              {errors.consent_contact}
            </p>
          </div>
          <div className="flex items-start gap-3">
            <input
              type="checkbox"
              id={fieldId("consent_ai_processing")}
              name="consent_ai_processing"
              checked={values.consent_ai_processing}
              onChange={setChecked("consent_ai_processing")}
              disabled={pending}
              className={checkboxClass}
            />
            <label htmlFor={fieldId("consent_ai_processing")} className="font-body text-sm text-foreground">
              {CONSENT_AI_TEXT}
            </label>
          </div>
        </fieldset>

        {/* Honeypot (R14.8): hidden from people and assistive tech. */}
        <div className={honeypotWrapper} aria-hidden="true">
          <label htmlFor="inquiry-website">Website</label>
          <input
            id="inquiry-website"
            type="text"
            name="website"
            tabIndex={-1}
            autoComplete="off"
            value={honeypot}
            onChange={(e) => setHoneypot(e.target.value)}
          />
        </div>

        <div>
          <Button type="submit" size="lg" disabled={pending || token.status === "loading"}>
            {pending ? (
              <>
                <span
                  aria-hidden="true"
                  className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
                />
                Sending…
              </>
            ) : (
              "Send inquiry"
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
