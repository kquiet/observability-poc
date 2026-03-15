import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';
import { Resource } from '@opentelemetry/resources';
import { trace } from '@opentelemetry/api';

class TraceManager {
  static #instance = null;

  constructor(config = {}) {
    if (TraceManager.#instance) {
      throw new Error(
        'Use TraceManager.getInstance(config) to access the singleton instance.'
      );
    }

    const {
      serviceName = 'default-service',
      component = 'frontend',
      exporterUrl = `${window.location.origin}/otel/v1/traces`,
      exporterHeaders = {},
      spanProcessorOptions = {
        scheduledDelayMillis: 5000,
        maxExportBatchSize: 512,
        maxQueueSize: 2048,
      },
    } = config;

    console.log('Initializing TraceManager with config:', config);

    const traceExporter = new OTLPTraceExporter({
      url: exporterUrl,
      headers: exporterHeaders,
    });

    // Set up a custom resource with the service name
    const tracerProvider = new WebTracerProvider({
      resource: new Resource({
        'service.name': serviceName,
        'component': component,
      }),
      spanProcessors: [
        new BatchSpanProcessor(traceExporter, spanProcessorOptions),
      ],
    });

    // Register the tracer provider globally
    tracerProvider.register();

    // Register automatic instrumentation: XMLHttpRequest, Fetch API, Document Load, User Interaction
    registerInstrumentations({
      instrumentations: [getWebAutoInstrumentations()],
    });
  }

  // Public method to get a tracer
  getTracer(name = 'default-tracer') {
    return trace.getTracer(name);
  }

  // Static method to enforce singleton and allow configuration
  static getInstance(config = {}) {
    if (!TraceManager.#instance) {
      TraceManager.#instance = new TraceManager(config);
    } else if (Object.keys(config).length > 0) {
      console.warn(
        'TraceManager instance is already initialized. Ignoring new config and returning the existing instance.'
      );
    }
    return TraceManager.#instance;
  }
}

export default TraceManager;
export { TraceManager };