import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { builtinModules } from 'module'; // Node.js built-in modules
import fs from 'fs';

const packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf-8'));
const externalDependencies = [
  ...Object.keys(packageJson.dependencies || {}).filter(dep => !['some-dep-to-include'].includes(dep)),
  ...builtinModules,
];

export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: 'src/index.js',
      name: 'OtelIntegrationLib',
      fileName: (format) => `otel-integration-lib.${format}.js`,
      formats: ['es', 'cjs', 'umd'],
    },
    rollupOptions: {
      external: externalDependencies,
      output: {
        globals: {
          '@opentelemetry/sdk-trace-web': 'otel.sdkTraceWeb',
          '@opentelemetry/sdk-trace-base': 'otel.sdkTraceBase',
          '@opentelemetry/exporter-trace-otlp-http': 'otel.exporterTraceOtlpHttp',
          '@opentelemetry/sdk-metrics': 'otel.sdkMetrics',
          '@opentelemetry/exporter-metrics-otlp-http': 'otel.exporterMetricsOtlpHttp',
          '@opentelemetry/instrumentation': 'otel.instrumentation',
          '@opentelemetry/auto-instrumentations-web': 'otel.autoInstrumentationsWeb',
          '@opentelemetry/resources': 'otel.resources',
          '@opentelemetry/api': 'otel.api',
        },
      },
    },
  },
})
