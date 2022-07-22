"""
Python script for fetching the current frame from the live-stream
"""
import os
import configparser
import cv2


def get_frame():
    """
    Fetches the current frame from the live-stream
    :return: The frame, as an object
    """
    config = configparser.ConfigParser()
    config.read("./tools/frame_fetcher/FETCHER_CONFIG.ini")
    youtube_url = config['DEFAULT']['YOUTUBE_URL']

    fetch_url = os.popen(f"youtube-dl -g {youtube_url}").read()

    capture_object = cv2.VideoCapture(fetch_url)
    _, frame = capture_object.read()

    return frame
