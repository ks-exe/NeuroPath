import { ApiClient, ApiError, buildApiPath } from "@neuropath/api-client";
import fc from "fast-check";
import { describe, expect, it, vi } from "vitest";

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), { status });
}

describe("api-client", () => {
  it("calls /api/v1/health and returns the body", async () => {
    const urls: string[] = [];
    const fetchImpl = vi.fn(async (url: RequestInfo | URL) => {
      urls.push(String(url));
      return jsonResponse(200, { status: "ok" });
    });
    const client = new ApiClient({ fetchImpl: fetchImpl as unknown as typeof fetch });
    await expect(client.health()).resolves.toEqual({ status: "ok" });
    expect(urls).toEqual(["/api/v1/health"]);
  });

  it("maps the error envelope to ApiError", async () => {
    const fetchImpl = vi.fn(async () =>
      jsonResponse(422, { code: "validation_error", message: "bad", fields: { a: "x" }, request_id: "r1" }),
    );
    const client = new ApiClient({ fetchImpl: fetchImpl as unknown as typeof fetch });
    const err = await client.get("/x").catch((e: unknown) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err).toMatchObject({ status: 422, code: "validation_error", requestId: "r1" });
  });

  it("rejects absolute URLs and dot segments", () => {
    for (const p of ["https://evil.test/x", "//evil.test", "health", "/../admin", "/a/../b"]) {
      expect(() => buildApiPath(p)).toThrow();
    }
  });

  // Property: every accepted path stays under /api/v1
  // Validates: Requirements 2.8
  it("only ever builds paths under /api/v1", () => {
    fc.assert(
      fc.property(fc.string(), (s) => {
        try {
          return buildApiPath(s).startsWith("/api/v1/");
        } catch {
          return true;
        }
      }),
      { numRuns: 100 },
    );
  });
});
