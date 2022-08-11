"""
Tests for Detect endpoint of model serving
"""
import pytest

from model_serving.app import app as flask_app_instance


@pytest.fixture()
def app():
    yield flask_app_instance


@pytest.fixture()
def client(app):
    return app.test_client()


class TestDetect:
    """
    Test case for detect
    """
    TEST_IMAGE_FILE_PATH = "./model_serving/tests/static/test_image.png"

    def test_no_image_file(self, client):
        """
        Tests the response from an invalid POST request to detect

        GIVEN a missing image in the POST request
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the status code is not 400
        :raise AssertionError: If the response data is not the expected value
        """
        response = client.post("/detect")

        assert response.status_code == 400

        expected_json_response = {
            "error": "NO_IMAGE_FILE",
            "description": "No image file was provided."
        }
        assert response.get_json() == expected_json_response

    def test_multiple_image_files(self, client):
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
            response = client.post("/detect", data={
                "image_file_1": image_file,
                "image_file_2": image_file
            })

        assert response.status_code == 400

        expected_json_response = {
            "error": "MULTIPLE_IMAGE_FILES",
            "description": "More than one image file was provided."
        }
        assert response.get_json() == expected_json_response

    def test_single_valid_image_file(self, client):
        """
        Tests the response from a valid POST request to detect

        GIVEN a POST request with a single valid image file
        WHEN receiving the response
        THEN the response is as expected

        :param client: The test client
        :raise AssertionError: If the status code is not 200
        :raise AssertionError: If the response data is not the expected value
        """
        with open(self.TEST_IMAGE_FILE_PATH, "rb") as image_file:
            response = client.post("/detect", data={
                "image_file": image_file
            })

        response_data_json = response.get_json()
        assert "labels" in response_data_json.keys()
        assert "detections" in response_data_json.keys()
