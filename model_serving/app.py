"""
Flask app for serving a REST API and interacting with the model
"""
from flask import Flask, request, jsonify, Response
import numpy as np
import cv2
import torch
import json

app = Flask(__name__)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./model_serving/model', force_reload=True)


def build_err_response(error: str, description: str, status_code: int):
    """
    Builds an JSON string to be returned following an error
    :param error: The error identifier
    :param description: A description of the error
    :param status_code: The HTTP status code to return
    :return: The built Response object
    """
    json_response = json.dumps({
        "error": error,
        "description": description
    })
    return Response(
        json_response, status=status_code, mimetype="application/json"
    )


@app.route('/health', methods=["GET"])
def health_check():
    return {"status": "ok"}


@app.route('/detect', methods=["POST"])
def detect():
    """
    Performs the inference using the model on the provided image
    :return: Response object
    """
    if len(request.files) > 1:
        return build_err_response("MULTIPLE_IMAGE_FILES",
                                  "More than one image file was provided.",
                                  400)
    elif len(request.files) < 1:
        return build_err_response("NO_IMAGE_FILE",
                                  "No image file was provided.",
                                  400)

    try:
        # Reading image from file-like buffer
        img_stream = request.files.get("image_file").stream
        img_stream.seek(0)
        img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Performing inference and returning results
        results = model(img)
        classes = {}
        for i in range(len(results.names)):
            classes[i] = results.names[i]

        predictions = results.pred[0]

        json_response = {
            "labels": classes,
            "detections": []
        }
        return Response(
            json.dumps(json_response),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return build_err_response("INVALID_IMAGE_FILE",
                                  "The image file provided is invalid.",
                                  400)
