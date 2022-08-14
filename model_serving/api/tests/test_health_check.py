"""
Tests for Health Check endpoint of model serving
"""
import pytest

from unittest.mock import MagicMock

from model_serving.api import create_app


@pytest.fixture()
def prod_model_app():
    mocked_model = MagicMock()
    # mocked_model.return_value.pred = [[[10, 10, 20, 20, 1, 0]]]
    # mocked_model.return_value.names = ["fish"]
    yield create_app(mocked_model)


@pytest.fixture()
def prod_model_client(prod_model_app):
    return prod_model_app.test_client()


class TestHealthCheck:
    """
    Test case for health check
    """
    def test_get_health_check(self, prod_model_client):
        """
        Tests the response from a valid GET request to the health check

        GIVEN a valid GET request to health check endpoint
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the response status code is not 200
        :raise AssertionError: If the response data is not the expected value
        """
        response = prod_model_client.get("/health")

        assert response.status_code == 200

        expected_json_response = {
            "status": "ok"
        }
        assert response.get_json() == expected_json_response
