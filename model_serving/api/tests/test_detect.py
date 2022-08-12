"""
Tests for Detect endpoint of model serving
"""
from unittest.mock import MagicMock

import pytest

from model_serving.api import create_app


@pytest.fixture(scope='function')
def prod_model_app():
    """
    Flask model-serving app created with production model
    :return: The created app
    """
    yield create_app()


@pytest.fixture()
def prod_model_client(prod_model_app):
    """
    Test client for prod_mode_app
    :param prod_model_app: The app to create the test client for
    :return: The created test client
    """
    return prod_model_app.test_client()


@pytest.fixture(scope='function')
def test_model_app_no_detections():
    """
    Flask model-serving app created with test model, no detections
    :return: The created app
    """
    mocked_model = MagicMock()
    mocked_model.pred = [[]]
    mocked_model.names = []
    yield create_app(mocked_model)


@pytest.fixture()
def test_model_client_no_detections(test_model_app_no_detections):
    """
    Test client for test_model_app_no_detections
    :param test_model_app_no_detections: The app to create the test client for
    :return: The created test client
    """
    return test_model_app_no_detections.test_client()


@pytest.fixture(scope='function')
def test_model_app_with_detection():
    """
    Flask model-serving app created with test model, with detection
    :return: The created app
    """
    mocked_model = MagicMock()
    mocked_model.return_value.pred = [[[10, 10, 20, 20, 1, 0]]]
    mocked_model.return_value.names = ["fish"]
    yield create_app(mocked_model)


@pytest.fixture()
def test_model_client_with_detection(test_model_app_with_detection):
    """
    Test client for test_model_app_with_detection
    :param test_model_app_with_detection: The app to create the test client for
    :return: The created test client
    """
    return test_model_app_with_detection.test_client()


class TestDetect:
    """
    Test cases requests to detect endpoint
    """
    TEST_IMAGE_FILE_PATH = "./model_serving/api/tests/static/test_image.png"

    def test_no_image_file(self, prod_model_client):
        """
        Tests the response from an invalid POST request to detect

        GIVEN a missing image in the POST request
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the status code is not 400
        :raise AssertionError: If the response data is not the expected value
        """
        response = prod_model_client.post("/detect")

        assert response.status_code == 400

        expected_json_response = {
            "error": "NO_IMAGE_FILE",
            "description": "No image file was provided."
        }
        assert response.get_json() == expected_json_response

    def test_multiple_image_files(self, prod_model_client):
        """
        Tests the response from an invalid POST request to detect

        GIVEN a POST request with multiple image files
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the status code is not 400
        :raise AssertionError: If the response data is not the expected value
        """
        with open(self.TEST_IMAGE_FILE_PATH, "rb") as image_file:
            response = prod_model_client.post("/detect", data={
                "image_file_1": image_file,
                "image_file_2": image_file
            })

        assert response.status_code == 400

        expected_json_response = {
            "error": "MULTIPLE_IMAGE_FILES",
            "description": "More than one image file was provided."
        }
        assert response.get_json() == expected_json_response

    def test_single_valid_image_file_no_detections(self, test_model_client_no_detections):
        """
        Tests the response from a valid POST request to detect with no detections

        GIVEN a POST request with a single valid image file and no objects to detect
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the status code is not 200
        :raise AssertionError: If the response data is not the expected value
        """
        with open(self.TEST_IMAGE_FILE_PATH, "rb") as image_file:
            response = test_model_client_no_detections.post("/detect", data={
                "image_file": image_file
            })

        assert response.status_code == 200

        expected_json_response = {
            "labels": {},
            "detections": []
        }
        assert response.get_json() == expected_json_response

    def test_single_valid_image_file_with_detection(self, test_model_client_with_detection):
        """
        Tests the response from a valid POST request to detect with a detection

        GIVEN a POST request with a single valid image file and one object to detect
        WHEN receiving the response
        THEN the response is as expected

        :param test_model_client_with_detection: The test client
        :raise AssertionError: If the status code is not 200
        :raise AssertionError: If the response data is not the expected value
        """
        with open(self.TEST_IMAGE_FILE_PATH, "rb") as image_file:
            response = test_model_client_with_detection.post("/detect", data={
                "image_file": image_file
            })

        expected_json_response = {
            "labels": {
                "0": "fish"
            },
            "detections": [
                {
                    "class_no": 0,
                    "confidence": 1.,
                    "x_center": 15,
                    "y_center": 15,
                    "width": 10,
                    "height": 10
                }
            ]
        }
        assert response.get_json() == expected_json_response
