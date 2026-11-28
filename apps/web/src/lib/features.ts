/**
 * Feature flags for the web app. These are non-secret, build-time constants.
 *
 * `authEnabled` gates the header Sign In link (R9.3). The Auth_Service is not
 * part of Phase 1, so it stays off until a later phase turns it on.
 */
export interface FeatureFlags {
  readonly authEnabled: boolean;
}

export const features: FeatureFlags = {
  authEnabled: false,
};
