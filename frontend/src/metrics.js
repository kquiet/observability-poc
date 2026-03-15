import { MetricManager } from '@zoo-dev/otel-integration-lib';

export const clickCounter = MetricManager.getInstance({
  serviceName: 'poc-frontend',
}).getMeter('poc-frontend').createCounter('button_click_count', {
  description: 'Counts the number of button clicks in the app',
});