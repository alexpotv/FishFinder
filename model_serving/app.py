"""
Flask app for serving a REST API and interacting with the model
"""
from flask import Flask, request, jsonify, Response
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

app = Flask(__name__)


@app.route('/health', methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "ok"
        }
    )


@app.route('/detect', methods=["POST"])
def detect():
    """
    Performs the inference using the model on the provided image
    :return: Response object
    """
    if len(request.files) > 1:
        return Response(
            {
                "error": "MULTIPLE_IMAGE_FILES",
                "description": "More than one image file was provided."
            },
            status=400
        )
    elif len(request.files) < 1:
        return Response(
            {
                "error": "INVALID_IMAGE_FILE",
                "description": "The provided image file is invalid."
            },
            status=400
        )

    print(request.files.get("image_file").stream.read())

    im = Image.open(request.files.get("image_file").stream)
    im.show()
