"""
Tests for Health Check endpoint of model serving
"""
import pytest

from model_serving.app import app as flask_app_instance


@pytest.fixture()
def app():
    yield flask_app_instance


@pytest.fixture()
def client(app):
    return app.test_client()


class TestHealthCheck:
    """
    Test case for health check
    """
    def test_get_health_check(self, client):
        """
        Tests the response from a valid GET request to the health check

        GIVEN a valid GET request to health check endpoint
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the response status code is not 200
        :raise AssertionError: If the response data is not the expected value
        """
        response = client.get("/health")

        assert response.status_code == 200

        expected_json_response = {
            "status": "ok"
        }
        assert response.get_json() == expected_json_response
