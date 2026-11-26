import { ApiClient } from "@neuropath/api-client";

/** Browser/same-origin client; requests go to /api/v1 and are proxied by Next. */
export const api = new ApiClient();
