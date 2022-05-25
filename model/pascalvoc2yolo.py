"""
Image annotation conversion tool to convert from PASCAL VOC format to YOLOv5-compatible
"""
import xml.etree.ElementTree as ET
import glob
import os
import json


BASE_PATH = "./model/data/"


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


classes = []
input_directories = os.listdir(BASE_PATH + "raw_data/")

if not os.path.isdir(BASE_PATH + "annotations"):
    os.mkdir(BASE_PATH + "annotations")

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

with open(BASE_PATH + 'annotations/classes.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(classes))
