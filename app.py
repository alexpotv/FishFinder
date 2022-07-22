"""
Streamlit app for interacting with the object detection model
"""
import streamlit as st
from tools.frame_fetcher.frame_fetcher import get_frame
import torch
import sys


st.set_page_config(layout="wide")

st.title("FishFinder")

col1, col2 = st.columns(2)

col1.header("Aquarium Live-Stream")

col1.markdown("This is the live-stream from the Monterey Bay Aquarium.")

col1.video("https://www.youtube.com/watch?v=zCt2V-bwDRE")

col2.header("Frame Analysis")

col2.markdown("Click the button below to fetch a frame from the stream and analyze it.")

col2.button("Analyze frame", on_click=None)

col2.subheader("Result")

with st.spinner("Getting the latest frame..."):
    image = get_frame()
    st.image(image)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s', force_reload=True)
    results = model(image)
    results.display(render=True)
    st.image(results.imgs[0])
    st.text(results)
