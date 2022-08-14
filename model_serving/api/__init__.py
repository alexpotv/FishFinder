"""
Flask application factory
"""
import torch
from flask import Flask
from .routes import route_blueprint


def create_app(testing_model=None):

    app = Flask(__name__)
    if testing_model:
        app.config['MODEL'] = testing_model
    else:
        app.config['MODEL'] = torch.hub.load('ultralytics/yolov5', 'custom', path='./api/model', force_reload=False, skip_validation=True)

    app.register_blueprint(route_blueprint)

    return app
