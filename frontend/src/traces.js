import { TraceManager } from '@zoo-dev/otel-integration-lib';

export const tracer = TraceManager.getInstance({
  serviceName: 'poc-frontend',
}).getTracer('poc-frontend');