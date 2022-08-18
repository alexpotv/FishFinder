# FishFinder

[![Tests - Model Serving](https://github.com/alexpotv/FishFinder/actions/workflows/model_serving_tests.yaml/badge.svg?branch=main)](https://github.com/alexpotv/FishFinder/actions/workflows/model_serving_tests.yaml)

**FishFinder** is a computer vision project based on images from [Monterey Bay Aquarium's live-streaming camera](https://youtu.be/zCt2V-bwDRE).

![example](https://user-images.githubusercontent.com/59039919/184552999-84656ff3-c7af-4395-a8dd-b74fe1c7b854.jpeg)

## Interacting with FishFinder

### Running the model with Docker-Compose

To run the model via Docker-Compose, run the following commands:

`cd model_serving`

`docker-compose build`

`docker-compose up`

### Interacting with the model-serving API

To interact with the model-serving API, send HTTP requests according to the **[API Reference](https://github.com/alexpotv/FishFinder/wiki/Model-API-Reference)**.

## Model

The model used for object detection is **[YoloV5, by Ultralytics](https://github.com/ultralytics/yolov5)**. Feel free to check out their GitHub repository to learn more about this model.

### Dataset

The model has been trained on a custom dataset, composed of images from the Aquarium, which have been manually annotated.
