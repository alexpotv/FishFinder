"""
Streamlit app for interacting with the object detection model
"""
import streamlit as st
from tools.frame_fetcher.frame_fetcher import get_frame
import torch
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
youtube_url = config['DEFAULT']['YOUTUBE_URL']

_, col2, _ = st.columns([0.3, 0.4, 0.3])

col2.title("FishFinder")

col2.header("Aquarium Live-Stream")
col2.markdown("This is the live-stream from the Monterey Bay Aquarium.")

col2.video(youtube_url)

col2.header("Frame Analysis")
col2.markdown("Click the button below to fetch a frame from the stream and analyze it.")
col2.button("Analyze frame", on_click=None)

col2.subheader("Result")

with st.spinner("Getting the latest frame..."):
    image = get_frame()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s', force_reload=True)
    results = model(image)
    results.display(render=True)
    col2.image(results.imgs[0], use_column_width=True)
