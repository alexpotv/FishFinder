"""
Frame fetcher tool for recuperating frames from a web-based livestream
"""
import os
import datetime
import configparser

config = configparser.ConfigParser()
config.read("./tools/frame_fetcher/FETCHER_CONFIG.ini")

START_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
os.mkdir(f"./model/data/raw_data/{START_TIME}")

os.system(f"ffmpeg -i {config['DEFAULT']['FETCH_URL']} -vf fps=1/{config['DEFAULT']['TIME_DELAY']} "
          f"-t {config['DEFAULT']['TOTAL_DURATION']} model/data/raw_data/{START_TIME}/out%d.png")
