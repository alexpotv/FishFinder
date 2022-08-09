"""
Flask app for serving a REST API and interacting with the model
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify(
        {
            "status": "ok"
        }
    )
