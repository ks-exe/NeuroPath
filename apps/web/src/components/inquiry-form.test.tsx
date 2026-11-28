import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { ApiError, type InquiryReceipt, type InquiryRequest } from "@neuropath/api-client";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { InquiryForm, type ServiceHintOption } from "@/components/inquiry-form";
import { emptyInquiry, parseServiceHint, retryMessage, toInquiryRequest } from "@/lib/inquiry";

const TOKEN_PATH = "/public/inquiries/submission-token";
const SUBMIT_PATH = "/public/inquiries";

const mock = vi.hoisted(() => ({
  post: vi.fn(),
  tokens: [] as string[],
  submit: (async () => undefined) as (body: unknown) => Promise<unknown>,
}));

vi.mock("@/lib/api", () => ({ api: { post: mock.post } }));

const serviceOptions: ServiceHintOption[] = [
  { id: "A", name: "Group A" },
  { id: "B", name: "Group B" },
];

const receipt: InquiryReceipt = { project_inquiry_id: "pi-1", project_id: "p-1", status_label: "Received" };

function apiError(status: number, fields: Record<string, string> | null = null, retryAfter: number | null = null) {
  return new ApiError(status, { code: "error", message: "Request failed.", fields, request_id: "req-123" }, retryAfter);
}

beforeEach(() => {
  mock.tokens = ["tok-1", "tok-2", "tok-3"];
  mock.submit = async () => receipt;
  mock.post.mockReset();
  mock.post.mockImplementation((path: string, body?: unknown) => {
    if (path === TOKEN_PATH) return Promise.resolve({ submission_token: mock.tokens.shift() ?? "tok-x" });
    if (path === SUBMIT_PATH) return mock.submit(body);
    return Promise.reject(new Error(`unexpected path ${path}`));
  });
});

const el = <T extends HTMLElement = HTMLInputElement>(name: string) => document.getElementById(`inquiry-${name}`) as T;
const submitButton = () => screen.getByRole("button", { name: /send inquiry|sending/i });
const submitCalls = () => mock.post.mock.calls.filter(([path]) => path === SUBMIT_PATH);
const firstBody = () => submitCalls()[0]?.[1] as InquiryRequest;
const tokenCalls = () => mock.post.mock.calls.filter(([path]) => path === TOKEN_PATH);

async function renderForm(initialServiceHint: "" | "A" | "B" = "") {
  render(<InquiryForm initialServiceHint={initialServiceHint} serviceOptions={serviceOptions} />);
  await waitFor(() => expect(submitButton()).toBeEnabled());
}

function fillValid() {
  fireEvent.change(el("name"), { target: { value: "Ada Lovelace" } });
  fireEvent.change(el("email"), { target: { value: "ada@example.com" } });
  fireEvent.change(el("title"), { target: { value: "Inventory forecasting" } });
  fireEvent.change(el<HTMLTextAreaElement>("problem_description"), {
    target: { value: "We cannot predict stock levels across our stores." },
  });
  fireEvent.click(el("consent_contact"));
}

function submit() {
  fireEvent.click(submitButton());
}

function expectValuesKept() {
  expect(el("name")).toHaveValue("Ada Lovelace");
  expect(el("email")).toHaveValue("ada@example.com");
  expect(el("title")).toHaveValue("Inventory forecasting");
  expect(el("problem_description")).toHaveValue("We cannot predict stock levels across our stores.");
  expect(el("consent_contact")).toBeChecked();
}

describe("InquiryForm client validation (R14.4)", () => {
  it("shows field errors, focuses the first invalid field, announces a summary and does not submit", async () => {
    await renderForm();
    submit();

    for (const name of ["name", "email", "title", "problem_description", "consent_contact"]) {
      expect(document.getElementById(`inquiry-${name}-error`)?.textContent).toMatch(/\w/);
    }
    expect(el("name")).toHaveAttribute("aria-invalid", "true");
    await waitFor(() => expect(document.activeElement).toBe(el("name")));
    expect(screen.getByRole("status")).toHaveTextContent(/The form has 5 errors/);
    expect(submitCalls()).toHaveLength(0);
  });
});

describe("InquiryForm API errors keep values (R14.5, R14.7)", () => {
  it("maps a 422 field error onto the email field", async () => {
    mock.submit = async () => {
      throw apiError(422, { email: "This email domain is not accepted." });
    };
    await renderForm();
    fillValid();
    submit();

    await waitFor(() => expect(el("email-error")).toHaveTextContent("This email domain is not accepted."));
    expect(el("email")).toHaveAttribute("aria-invalid", "true");
    expectValuesKept();
  });

  it("shows a generic message with the request id on a 500", async () => {
    mock.submit = async () => {
      throw apiError(500);
    };
    await renderForm();
    fillValid();
    submit();

    await waitFor(() =>
      expect(screen.getByText(/Something went wrong/, { selector: "[role=alert] p" })).toHaveTextContent(
        "Reference: req-123",
      ),
    );
    expect(screen.getByRole("status")).toHaveTextContent("Reference: req-123");
    expectValuesKept();
  });

  it("shows the retry message on a 429", async () => {
    mock.submit = async () => {
      throw apiError(429, null, 120);
    };
    await renderForm();
    fillValid();
    submit();

    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("try again in 2 minutes"));
    expect(screen.getAllByText(/try again in 2 minutes/).length).toBeGreaterThan(0);
    expectValuesKept();
  });

  it("reuses the same submission token when retrying after a failure (R14.14)", async () => {
    let attempt = 0;
    mock.submit = async () => {
      attempt += 1;
      if (attempt === 1) throw apiError(500);
      return receipt;
    };
    await renderForm();
    fillValid();
    submit();
    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent(/Something went wrong/));
    await waitFor(() => expect(submitButton()).toBeEnabled());
    submit();
    await waitFor(() => expect(screen.getByText(/Your inquiry was received/)).toBeInTheDocument());

    const tokens = submitCalls().map(([, body]) => (body as InquiryRequest).submission_token);
    expect(tokens).toEqual(["tok-1", "tok-1"]);
  });
});

describe("InquiryForm success (R14.6)", () => {
  it("shows the confirmation with the status label, clears inputs and requests a new token", async () => {
    await renderForm();
    fillValid();
    submit();

    await waitFor(() => expect(screen.getByText(/Status: Received/)).toBeInTheDocument());
    expect(screen.getByText(/Your inquiry was received/)).toBeInTheDocument();
    expect(el("name")).toHaveValue("");
    expect(el("email")).toHaveValue("");
    expect(el("problem_description")).toHaveValue("");
    expect(el("consent_contact")).not.toBeChecked();
    await waitFor(() => expect(tokenCalls()).toHaveLength(2));
  });
});

describe("InquiryForm pending state (R14.13)", () => {
  it("disables the button and inputs while the submission is in flight", async () => {
    let resolve: (value: InquiryReceipt) => void = () => undefined;
    mock.submit = () => new Promise<InquiryReceipt>((r) => (resolve = r));
    await renderForm();
    fillValid();
    submit();

    await waitFor(() => expect(submitButton()).toHaveTextContent("Sending"));
    expect(submitButton()).toBeDisabled();
    expect(el("name")).toBeDisabled();
    expect(el("problem_description")).toBeDisabled();
    expect(el("consent_contact")).toBeDisabled();

    await act(async () => resolve(receipt));
    await waitFor(() => expect(screen.getByText(/Your inquiry was received/)).toBeInTheDocument());
  });
});

describe("InquiryForm service hint and honeypot", () => {
  it("preselects the hint, sends it, and has no technology category field", async () => {
    await renderForm("B");
    expect(el<HTMLSelectElement>("service_hint")).toHaveValue("B");
    expect(document.querySelector('[name*="techn" i], [name*="category" i]')).toBeNull();

    fillValid();
    submit();
    await waitFor(() => expect(submitCalls()).toHaveLength(1));
    expect(firstBody().service_hint).toBe("B");
  });

  it("clears the hint and omits it from the request body", async () => {
    await renderForm("B");
    fireEvent.click(screen.getByRole("button", { name: "Clear service area" }));
    expect(el<HTMLSelectElement>("service_hint")).toHaveValue("");

    fillValid();
    submit();
    await waitFor(() => expect(submitCalls()).toHaveLength(1));
    expect(firstBody()).not.toHaveProperty("service_hint");
  });

  it("renders a hidden honeypot and sends it as website", async () => {
    await renderForm();
    const honeypot = document.querySelector<HTMLInputElement>('input[name="website"]');
    expect(honeypot).not.toBeNull();
    expect(honeypot).toHaveAttribute("tabindex", "-1");
    expect(honeypot?.closest('[aria-hidden="true"]')).not.toBeNull();

    fillValid();
    fireEvent.change(honeypot as HTMLInputElement, { target: { value: "spam.example" } });
    submit();
    await waitFor(() => expect(submitCalls()).toHaveLength(1));
    expect(firstBody().website).toBe("spam.example");
  });
});

describe("inquiry helpers", () => {
  it("parseServiceHint accepts group ids A to F only", () => {
    expect(parseServiceHint("b")).toBe("B");
    expect(parseServiceHint(["F", "A"])).toBe("F");
    expect(parseServiceHint("G")).toBe("");
    expect(parseServiceHint(undefined)).toBe("");
    expect(parseServiceHint(42)).toBe("");
  });

  it("retryMessage rounds up to whole minutes", () => {
    expect(retryMessage(60)).toContain("try again in 1 minute.");
    expect(retryMessage(61)).toContain("try again in 2 minutes.");
    expect(retryMessage(null)).toContain("a few minutes");
    expect(retryMessage(0)).toContain("a few minutes");
  });

  it("toInquiryRequest trims values and omits empty optional fields", () => {
    const values = {
      ...emptyInquiry(),
      name: " Ada ",
      email: "ada@example.com",
      title: "T",
      problem_description: "Problem",
      company: "  ",
      budget_range: "10k",
      consent_contact: true,
    };
    const body = toInquiryRequest(values, "tok", "");
    expect(body.name).toBe("Ada");
    expect(body.budget_range).toBe("10k");
    expect(body.website).toBe("");
    for (const key of ["company", "service_hint", "desired_outcome", "preferred_timeline"]) {
      expect(body).not.toHaveProperty(key);
    }
  });
});
