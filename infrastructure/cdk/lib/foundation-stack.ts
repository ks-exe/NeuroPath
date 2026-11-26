import { Stack, StackProps, aws_budgets as budgets } from 'aws-cdk-lib';
import { Construct } from 'constructs';

export interface FoundationStackProps extends StackProps {
  readonly environment: 'dev' | 'staging' | 'prod';
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function requireContext(scope: Construct, key: string): string {
  const value: unknown = scope.node.tryGetContext(key);
  if (value === undefined || value === null || String(value).trim() === '') {
    throw new Error(
      `Missing required CDK context "${key}". Pass it with "-c ${key}=<value>". ` +
        'No default is provided on purpose; real values must come from the Founder.',
    );
  }
  return String(value).trim();
}

/**
 * Foundation stack.
 *
 * The cost budget is intentionally the first and only resource. All other
 * resources are added in later tasks. Deploying this stack (or any other)
 * requires the Founder's written authorization (R3.6).
 */
export class FoundationStack extends Stack {
  constructor(scope: Construct, id: string, props: FoundationStackProps) {
    super(scope, id, props);

    const limitRaw = requireContext(this, 'budgetLimitUsd');
    const limitUsd = Number(limitRaw);
    if (!Number.isFinite(limitUsd) || limitUsd <= 0) {
      throw new Error(
        `Invalid CDK context "budgetLimitUsd=${limitRaw}". Expected a positive number of US dollars.`,
      );
    }

    const alertEmail = requireContext(this, 'budgetAlertEmail');
    if (!EMAIL_PATTERN.test(alertEmail)) {
      throw new Error(
        `Invalid CDK context "budgetAlertEmail=${alertEmail}". Expected an email address.`,
      );
    }

    const subscribers = [{ subscriptionType: 'EMAIL', address: alertEmail }];

    new budgets.CfnBudget(this, 'MonthlyCostBudget', {
      budget: {
        budgetName: `neuropath-${props.environment}-monthly-cost`,
        budgetType: 'COST',
        timeUnit: 'MONTHLY',
        budgetLimit: { amount: limitUsd, unit: 'USD' },
      },
      notificationsWithSubscribers: [
        {
          notification: {
            notificationType: 'ACTUAL',
            comparisonOperator: 'GREATER_THAN',
            threshold: 80,
            thresholdType: 'PERCENTAGE',
          },
          subscribers,
        },
        {
          notification: {
            notificationType: 'FORECASTED',
            comparisonOperator: 'GREATER_THAN',
            threshold: 100,
            thresholdType: 'PERCENTAGE',
          },
          subscribers,
        },
      ],
    });
  }
}
