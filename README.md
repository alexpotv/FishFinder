# FishFinder
Computer vision project based on images from Monterey Bay Aquarium's live-streaming camera.

## For training

From project root:

`python yolov5/train.py --img 640 --batch 1 --epochs 5 --data model/dataset.yaml --weights yolov5s.pt --hyp model/hyp.scratch.yaml`
