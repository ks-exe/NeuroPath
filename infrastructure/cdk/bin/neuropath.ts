#!/usr/bin/env node
/**
 * NeuroPath CDK app entry point.
 *
 * Synth only. Deploying any stack requires the Founder's written
 * authorization (R3.6). No credentials or environment lookups are needed
 * for `cdk synth`.
 *
 * Context:
 *   -c env=dev|staging|prod      (default: dev)
 *   -c owner=<name>              (default: founder)
 *   -c account=<id> -c region=<region>  (optional; env-agnostic if unset)
 *   -c budgetLimitUsd=<number>   (required)
 *   -c budgetAlertEmail=<email>  (required)
 */
import { App, Aspects, Tags } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';
import { FoundationStack } from '../lib/foundation-stack';

const ENVIRONMENTS = ['dev', 'staging', 'prod'] as const;
type EnvironmentName = (typeof ENVIRONMENTS)[number];

function isEnvironmentName(value: string): value is EnvironmentName {
  return (ENVIRONMENTS as readonly string[]).includes(value);
}

const app = new App();

const envContext = String(app.node.tryGetContext('env') ?? 'dev');
if (!isEnvironmentName(envContext)) {
  throw new Error(
    `Invalid context "env=${envContext}". Expected one of: ${ENVIRONMENTS.join(', ')}.`,
  );
}
const environment: EnvironmentName = envContext;
const owner = String(app.node.tryGetContext('owner') ?? 'founder');

const account = app.node.tryGetContext('account') as string | undefined;
const region = app.node.tryGetContext('region') as string | undefined;

new FoundationStack(app, `NeuroPath-Foundation-${environment}`, {
  environment,
  // Env-agnostic unless account/region are given explicitly via context.
  env: account || region ? { account, region } : undefined,
  description: `NeuroPath foundation stack (${environment}). Deploy only with the Founder's written authorization.`,
});

Tags.of(app).add('project', 'neuropath');
Tags.of(app).add('environment', environment);
Tags.of(app).add('owner', owner);

Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));

app.synth();
