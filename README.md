# FishFinder

[![Tests - Model Serving](https://github.com/alexpotv/FishFinder/actions/workflows/model_serving_tests.yaml/badge.svg?branch=main)](https://github.com/alexpotv/FishFinder/actions/workflows/model_serving_tests.yaml)

**FishFinder** is a computer vision project based on images from Monterey Bay Aquarium's live-streaming camera.

## Interacting with FishFinder

### Installing the requirements

To launch the app, make sure the environment you are using is up-to-date py running the following command from the root 
of the project:

```pip install -r requirements.txt```

### Launching the Streamlit interface

To launch the Streamlit web interface locally, run the following command from the root of the project:

```streamlit run app.py```

Streamlit will open a new browser tab with the interface. If the browser tab does not pop up, simply take a look at the 
console, where the local URL will be displayed.

## Model

The model used for object detection is **[YoloV5, by Ultralytics](https://github.com/ultralytics/yolov5)**. Feel free to check out their GitHub repository to learn more about this model.

### Dataset

The model has been trained on a custom dataset, composed of images from the Aquarium, which have been manually annotated.
