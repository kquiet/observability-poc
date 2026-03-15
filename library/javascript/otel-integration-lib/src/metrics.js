import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { metrics } from '@opentelemetry/api';

class MetricManager {
  static #instance = null;

  constructor(config = {}) {
    if (MetricManager.#instance) {
      throw new Error(
        'Use MetricsManager.getInstance(config) to access the singleton instance.'
      );
    }

    // Destructure config with default values
    const {
      serviceName = 'poc-frontend',
      component = 'frontend',
      exporterUrl = `${window.location.origin}/otel/v1/metrics`,
      exporterHeaders = {},
      exportIntervalMillis = 15000,
    } = config;

    console.log('Initializing MetricManager with config:', config);

    // Set up the MeterProvider with the PeriodicExportingMetricReader
    const meterProvider = new MeterProvider({
      resource: new Resource({
        'service.name': serviceName,
        'component': component,
      }),
      readers: [
        new PeriodicExportingMetricReader({
          exporter: new OTLPMetricExporter({
            url: exporterUrl,
            header: exporterHeaders,
          }),
          exportIntervalMillis: exportIntervalMillis,
        }),
      ],
    });

    // Register the meter provider globally
    metrics.setGlobalMeterProvider(meterProvider);
  }

  // Public method to get a meter
  getMeter(name = 'default-meter') {
    return metrics.getMeter(name);
  }

  // Static method to enforce singleton and allow configuration
  static getInstance(config = {}) {
    if (!MetricManager.#instance) {
      MetricManager.#instance = new MetricManager(config);
    } else {
      console.warn(
        'MetricManager instance is already initialized. Ignoring new config and returning the existing instance.'
      );
    }
    return MetricManager.#instance;
  }
}

export default MetricManager;
export { MetricManager };