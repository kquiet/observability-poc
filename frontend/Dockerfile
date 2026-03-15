FROM node:20.17.0-bookworm-slim AS stage1-source
WORKDIR /app
COPY ./library/javascript/otel-integration-lib ./library/javascript/otel-integration-lib
COPY ./frontend ./frontend

FROM stage1-source AS stage2-build
RUN npm install -g pnpm

# Build the library first
WORKDIR /app/library/javascript/otel-integration-lib
RUN pnpm install && pnpm run build

# Build the frontend
WORKDIR /app/frontend
RUN pnpm install && pnpm run build

FROM nginx:1.27.2
ENV HTML_PATH=/var/www/html
WORKDIR ${HTML_PATH}
COPY ./frontend/resources/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=stage2-build /app/frontend/dist ${HTML_PATH}
