"""
Temp test of model loading
"""

import torch
from tools.frame_fetcher.frame_fetcher import get_frame

image = get_frame()
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=True)
model(image)

print("Done")