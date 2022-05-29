"""
Data splitting stage of pre-processing, which includes:
- Splitting training, testing, and validation data
- Converting annotations format from PascalVOC to YoloV5
- Creating expected directory structure for YoloV5 training
"""
import glob
import json
import os
import shutil
import xml.etree.ElementTree as ET

import pandas as pd
from fast_ml.model_development import train_valid_test_split

BASE_PATH = "./model/data/"
BASE_IMAGES_PATH = "./model/data/raw_data/"


def voc_to_yolo_bbox(bbox, w, h):
    """
    Converts a PASCAL VOC bounding box to YOLOv5 format
    :param bbox: The bounding box coordinates
    :param w: The width of the image
    :param h: The height of the image
    :return: The YOLOv5-formatted bounding box
    """
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_voc_bbox(bbox, w, h):
    """
    Converts a YOLOv5 bounding box to PASCAL VOC format
    :param bbox: The bounding box coordinates
    :param w: The width of the image
    :param h: The height of the image
    :return: The PASCAL VOC-formatted bounding box
    """
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def read_and_convert(filepath: str):
    """
    Reads and converts an annotation file
    :param filepath: The file path for the annotation file
    :return: The result
    """
    result = []

    tree = ET.parse(filepath)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        label = obj.find("name").text
        if label not in classes:
            classes.append(label)
        index = classes.index(label)
        pil_bbox = [int(x.text) for x in obj.find("bndbox")]
        yolo_bbox = voc_to_yolo_bbox(pil_bbox, width, height)
        bbox_string = " ".join([str(x) for x in yolo_bbox])
        result.append(f"{index} {bbox_string}")

    return result


classes = []
input_directories = os.listdir(BASE_PATH + "raw_data/")

annotation_files = glob.glob(BASE_IMAGES_PATH + "**/*.xml", recursive=True)
expected_image_files = [os.path.splitext(x)[0] + ".png" for x in annotation_files]

# Verify that each annotation file corresponds to an image file
for expected_image_file in expected_image_files:
    if not os.path.exists(expected_image_file):
        raise ValueError("Some annotations files do not have an associated image.")

# Create directory structure
os.mkdir(f"{BASE_PATH}images")
os.mkdir(f"{BASE_PATH}images/train")
os.mkdir(f"{BASE_PATH}images/val")
os.mkdir(f"{BASE_PATH}images/test")

os.mkdir(f"{BASE_PATH}labels")
os.mkdir(f"{BASE_PATH}labels/train")
os.mkdir(f"{BASE_PATH}labels/val")
os.mkdir(f"{BASE_PATH}labels/test")

# Split the training, validating and testing data
files = pd.DataFrame({"Images": expected_image_files, "Annotations": annotation_files})
X_train, y_train, X_valid, y_valid, X_test, y_test = train_valid_test_split(files,
                                                                            target="Annotations",
                                                                            train_size=0.8,
                                                                            valid_size=0.1,
                                                                            test_size=0.1)

# Copy training, validation and testing images to new location
for train_file in X_train.Images:
    dirname = os.path.dirname(train_file).split('/')[-1]
    shutil.copy(train_file, f"{BASE_PATH}images/train/{dirname}-{os.path.basename(train_file)}")
for valid_file in X_valid.Images:
    dirname = os.path.dirname(valid_file).split('/')[-1]
    shutil.copy(valid_file, f"{BASE_PATH}images/val/{dirname}-{os.path.basename(valid_file)}")
for test_file in X_test.Images:
    dirname = os.path.dirname(test_file).split('/')[-1]
    shutil.copy(test_file, f"{BASE_PATH}images/test/{dirname}-{os.path.basename(test_file)}")

# Convert annotations and move to labels directory
for train_annotation in y_train:
    dirname = os.path.dirname(train_annotation).split('/')[-1]
    result = read_and_convert(train_annotation)
    if result:
        with open(f"{BASE_PATH}labels/train/{dirname}-{os.path.basename(train_annotation).split('.')[0]}.txt", "w",
                  encoding="utf-8") as f:
            f.write("\n".join(result))
for valid_annotation in y_valid:
    dirname = os.path.dirname(valid_annotation).split('/')[-1]
    result = read_and_convert(valid_annotation)
    if result:
        with open(f"{BASE_PATH}labels/val/{dirname}-{os.path.basename(valid_annotation).split('.')[0]}.txt", "w",
                  encoding="utf-8") as f:
            f.write("\n".join(result))
for test_annotation in y_test:
    dirname = os.path.dirname(test_annotation).split('/')[-1]
    result = read_and_convert(test_annotation)
    if result:
        with open(f"{BASE_PATH}labels/test/{dirname}-{os.path.basename(test_annotation).split('.')[0]}.txt", "w",
                  encoding="utf-8") as f:
            f.write("\n".join(result))

"""
for directory in input_directories:
    if not os.path.isdir(BASE_PATH + f"annotations/{directory}"):
        os.mkdir(BASE_PATH + F"annotations/{directory}")

    for file in glob.glob(BASE_PATH + f"raw_data/{directory}/*.xml"):
        result = []

        tree = ET.parse(file)
        root = tree.getroot()
        width = int(root.find("size").find("width").text)
        height = int(root.find("size").find("height").text)

        for obj in root.findall('object'):
            label = obj.find("name").text
            if label not in classes:
                classes.append(label)
            index = classes.index(label)
            pil_bbox = [int(x.text) for x in obj.find("bndbox")]
            yolo_bbox = voc_to_yolo_bbox(pil_bbox, width, height)
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

        filename = os.path.basename(file).split('.')[0]
        if result:
            with open(BASE_PATH + f"annotations/{directory}/{filename}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(result))
"""

with open(f"{BASE_PATH}classes.txt", 'w', encoding='utf8') as f:
    f.write(json.dumps(classes))
