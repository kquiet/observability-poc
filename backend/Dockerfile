# prepare dependency
FROM python:3.11.10-bookworm AS stage1

##prepare poetry for dependency install
RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy the local library first because it's a dependency of pyproject.toml
COPY library/python/fastapi_metrics_prometheus /library/python/fastapi_metrics_prometheus
COPY backend/pyproject.toml ./

## install runtime dependency only
RUN poetry -v install --only main --no-root
RUN .venv/bin/opentelemetry-bootstrap -a install
RUN rm -rf $POETRY_CACHE_DIR


# build final image using slim version
FROM python:3.11.10-bookworm AS stage2
ARG BUILD_BY=manual
LABEL build-by=${BUILD_BY}

ENV VIRTUAL_ENV="/app/.venv" \
    PATH="/app/.venv/bin:${PATH}" \
    TZ=Asia/Taipei \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    OTEL_RESOURCE_ATTRIBUTES="service.name=poc-backend" \
    OTEL_TRACES_EXPORTER="console" \
    OTEL_METRICS_EXPORTER="console" \
    OTEL_PYTHON_LOG_CORRELATION="true" \
    OTEL_PYTHON_LOG_LEVEL="debug"

## handle for timezone & localtime
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

WORKDIR /app

## copy runtime dependency from stage1
COPY --from=stage1 ["${VIRTUAL_ENV}", "${VIRTUAL_ENV}"]

## copy project python
COPY ["backend/app", "./app"]
COPY ["backend/main.py", "backend/logging_config.yaml", "./"]

## use CMD for future override when needed
CMD ["opentelemetry-instrument", "python", "main.py"]
