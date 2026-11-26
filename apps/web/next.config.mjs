/**
 * API_BASE_URL is server-only (no NEXT_PUBLIC_ prefix). The browser calls
 * same-origin /api/v1 and Next proxies it to the API (R2.8).
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@neuropath/api-client", "@neuropath/design-tokens", "@neuropath/ui"],
  async rewrites() {
    const apiBase = process.env.API_BASE_URL ?? "http://localhost:8000";
    return [{ source: "/api/v1/:path*", destination: `${apiBase}/api/v1/:path*` }];
  },
};

export default nextConfig;
