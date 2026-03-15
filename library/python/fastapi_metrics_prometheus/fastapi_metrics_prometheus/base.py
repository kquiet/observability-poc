import time
from typing import Tuple

from prometheus_client import (
    REGISTRY,
    CONTENT_TYPE_LATEST,
    generate_latest,
    Counter,
    Gauge,
    Histogram,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

INFO = Gauge("api_app_info", "API application information.", [])
REQUESTS = Counter(
    "api_requests_total",
    "Total count of requests by method and path.",
    ["method", "path"],
)
RESPONSES = Counter(
    "api_responses_total",
    "Total count of responses by method, path and status codes.",
    ["method", "path", "status_code"],
)
REQUESTS_PROCESSING_TIME = Histogram(
    "api_requests_duration_seconds",
    "Histogram of requests processing time by path (in seconds)",
    ["method", "path"],
)
EXCEPTIONS = Counter(
    "api_exceptions_total",
    "Total count of exceptions raised by path and exception type",
    ["method", "path", "exception_type"],
)
REQUESTS_IN_PROGRESS = Gauge(
    "api_requests_in_progress",
    "Gauge of requests by method and path currently being processed",
    ["method", "path"],
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        INFO.inc()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path, is_handled_path = self.get_path(request)

        if not is_handled_path:
            return await call_next(request)

        REQUESTS_IN_PROGRESS.labels(method=method, path=path).inc()
        REQUESTS.labels(method=method, path=path).inc()
        before_time = time.perf_counter()
        try:
            response = await call_next(request)
        except BaseException as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(method=method, path=path, exception_type=type(e).__name__).inc()
            raise e from None
        else:
            status_code = response.status_code
            after_time = time.perf_counter()

            REQUESTS_PROCESSING_TIME.labels(method=method, path=path).observe(
                after_time - before_time
            )
        finally:
            RESPONSES.labels(method=method, path=path, status_code=status_code).inc()
            REQUESTS_IN_PROGRESS.labels(method=method, path=path).dec()

        return response

    @staticmethod
    def get_path(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False


def metrics(request: Request) -> Response:
    return Response(
        generate_latest(REGISTRY),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )
