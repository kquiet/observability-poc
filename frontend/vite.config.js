import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 9080,
    hmr: {
      overlay: false,
    },
    proxy: { // proxy backend api requests for local development
      '/backend': {
        target: 'http://127.0.0.1:8080', // Backend server URL
        changeOrigin: true, // Change the Origin header to match the target
        rewrite: (path) => path.replace(/^\/backend/, ''), // Rewrite the path
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // Add custom headers if backend need these:
            proxyReq.setHeader('Host', req.headers.host);
            proxyReq.setHeader('X-Real-IP', req.socket.remoteAddress);
            proxyReq.setHeader('X-Forwarded-For', req.headers['x-forwarded-for'] || req.socket.remoteAddress);
            proxyReq.setHeader('X-Forwarded-Proto', req.headers['x-forwarded-proto'] || (req.socket.encrypted ? 'https' : 'http'));
          });
        },
      },
      // Proxy for OpenTelemetry Collector trace requests
      '/otel': {
        target: 'http://127.0.0.1:14318', // OpenTelemetry Collector URL
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/otel/, ''), // Remove '/otel' prefix
      },
    }
  }
})
