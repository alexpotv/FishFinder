"""
Frame fetcher tool for recuperating frames from a web-based livestream
"""
import os
import datetime
import configparser
from colorama import Fore


def print_log(msg_type: str, message: str):
    """
    Logs a message to the console
    :param msg_type: The message log type
    :param message: The message to log
    :return: None
    """
    color_type_mapping = {
        "LOG": Fore.CYAN,
        "OK": Fore.GREEN,
        "WARN": Fore.YELLOW
    }
    color = color_type_mapping.get(msg_type)
    if not color:
        color = ""

    print(f"{color}{datetime.datetime.now().strftime('%H:%M:%S')} - [{msg_type}] {message}")

print_log("LOG", "Reading configuration file...")
config = configparser.ConfigParser()
config.read("./tools/frame_fetcher/FETCHER_CONFIG.ini")
print_log("OK", "Configuration file read successfully!")

START_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
YOUTUBE_URL = config['DEFAULT']['YOUTUBE_URL']
TIME_DELAY = config['DEFAULT']['TIME_DELAY']
TOTAL_DURATION = config['DEFAULT']['TOTAL_DURATION']

print_log("LOG", "Creating direct live-stream URL for resource...")
FETCH_URL = os.popen(f"youtube-dl -g {YOUTUBE_URL}").read()
print_log("OK", "Live stream direct URL successfully created!")

print_log("LOG", f"Creating directory for {START_TIME} frame fetch run...")
os.mkdir(f"./model/data/raw_data/{START_TIME}")
print_log("OK", "Directory created successfully!")

print_log("LOG", f"Launching frame fetch run for {TOTAL_DURATION} seconds...")
os.system(f"ffmpeg -hide_banner -loglevel error -i \"{FETCH_URL}\" -vf fps=1/{TIME_DELAY} -t {TOTAL_DURATION} "
          f"model/data/raw_data/{START_TIME}/out%d.png")
print_log("OK", f"Finished {START_TIME} frame fetch run!")

print_log("WARN", "Remember to run \"dvc add\" to track newly added data files!")
