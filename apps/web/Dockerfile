# Build context: repository root (workspace packages are needed).
FROM node:20-alpine

ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /repo

COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/
COPY packages/api-client/package.json packages/api-client/
COPY packages/design-tokens/package.json packages/design-tokens/
RUN npm ci

COPY apps/web apps/web
COPY packages packages

# The rewrite destination is fixed at build time by Next.js, so API_BASE_URL
# must be present for the build as well as at runtime.
ARG API_BASE_URL=http://api:8000
ENV API_BASE_URL=${API_BASE_URL}
RUN npm run build --workspace @neuropath/web

ENV NODE_ENV=production
USER node
WORKDIR /repo/apps/web
EXPOSE 3000
CMD ["npx", "next", "start", "-H", "0.0.0.0", "-p", "3000"]
