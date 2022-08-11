"""
Flask application factory
"""
from flask import Flask
import torch


def create_app(testing_model=None):

    app = Flask(__name__)
    if testing_model:
        app.config['MODEL'] = testing_model
    else:
        app.config['MODEL'] = torch.hub.load('ultralytics/yolov5', 'custom', path='./model_serving/model',
                                             force_reload=True)

    from model_serving.routes import route_blueprint
    app.register_blueprint(route_blueprint)

    return app
