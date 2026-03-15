import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient
from starlette.responses import PlainTextResponse
from prometheus_client.parser import text_string_to_metric_families
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi_metrics_prometheus.base import PrometheusMiddleware, metrics


def create_app():
    app = Starlette()
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)

    async def test_endpoint(request):
        return PlainTextResponse("Test endpoint!")

    app.add_route("/test", test_endpoint)

    async def test_exception_endpoint(request):
        raise ValueError("an error occurred")

    app.add_route("/testexception", test_exception_endpoint)

    return app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_prometheus_middleware(client):
    # Send a request to non-existing endpoint
    client.get("/nonexist")

    # Send a request to the /test endpoint
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "Test endpoint!"

    # Send a request to /metrics endpoint to get metrics
    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    assert "Content-Type" in metrics_response.headers
    assert metrics_response.headers["Content-Type"] == CONTENT_TYPE_LATEST

    # Parse metrics
    metrics_output = metrics_response.text
    parsed_metrics = list(text_string_to_metric_families(metrics_output))

    # Check that the expected metrics are present and correct
    assert any(family.name == "api_app_info" for family in parsed_metrics)
    assert any(family.name == "api_requests" for family in parsed_metrics)
    assert any(family.name == "api_responses" for family in parsed_metrics)
    assert any(family.name == "api_requests_duration_seconds" for family in parsed_metrics)
    assert any(family.name == "api_requests_in_progress" for family in parsed_metrics)
    for family in parsed_metrics:
        if family.name == "api_app_info":
            assert len(family.samples) == 1
            assert family.samples[0].value == 1
        elif family.name == "api_requests":
            assert len(family.samples) == 2
            assert family.samples[0].labels.get("path") == "/test"
            assert family.samples[1].labels.get("path") == "/metrics"
            assert all(sample.value == 1 for sample in family.samples)
        elif family.name == "api_responses":
            assert len(family.samples) == 1
            assert family.samples[0].labels.get("path") == "/test"
            assert family.samples[0].value == 1
        elif family.name == "api_requests_in_progress":
            assert len(family.samples) == 2
            assert family.samples[0].labels.get("path") == "/test"
            assert family.samples[0].value == 0
            assert family.samples[1].labels.get("path") == "/metrics"
            assert family.samples[1].value == 1
        elif family.name == "api_requests_duration_seconds":
            assert len(family.samples) >= 3
            sample_count_test = next(
                (
                    sample
                    for sample in family.samples
                    if sample.name == "api_requests_duration_seconds_count"
                    and sample.labels.get("path") == "/test"
                ),
                None,
            )
            assert sample_count_test.value == 1
            sample_summary_test = next(
                (
                    sample
                    for sample in family.samples
                    if sample.name == "api_requests_duration_seconds_sum"
                    and sample.labels.get("path") == "/test"
                ),
                None,
            )
            assert sample_summary_test.value > 0
            # no metrics for /metrics
            sample_count_metrics = next(
                (
                    sample
                    for sample in family.samples
                    if sample.name == "api_requests_duration_seconds_count"
                    and sample.labels.get("path") == "/metrics"
                ),
                None,
            )
            assert sample_count_metrics is None
            sample_summary_metrics = next(
                (
                    sample
                    for sample in family.samples
                    if sample.name == "api_requests_duration_seconds_sum"
                    and sample.labels.get("path") == "/metrics"
                ),
                None,
            )
            assert sample_summary_metrics is None


def test_prometheus_exception_handling(client):
    # Send a request to /testexception to trigger an exception
    with pytest.raises(Exception):
        client.get("/testexception")

    # get metrics
    metrics_response = client.get("/metrics")
    metrics_output = metrics_response.text
    parsed_metrics = list(text_string_to_metric_families(metrics_output))

    # Check if exception metric exists and correct
    assert any(family.name == "api_exceptions" for family in parsed_metrics)
    for family in parsed_metrics:
        if family.name == "api_exceptions":
            assert len(family.samples) == 1
            assert family.samples[0].value == 1
