"""
Frame fetcher tool for recuperating frames from a web-based livestream
"""
import os
import datetime
import configparser
from time import sleep

from colorama import Fore
from frame_fetcher import get_frame
import cv2


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


FETCHER_CONFIG_PATH = "./tools/frame_fetcher/FETCHER_CONFIG.ini"
CONFIG_PATH = "config.ini"

print_log("LOG", "Reading configuration files...")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
fetcher_config = configparser.ConfigParser()
fetcher_config.read(FETCHER_CONFIG_PATH)
print_log("OK", "Configuration files read successfully!")

START_TIME = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
YOUTUBE_URL = config['DEFAULT']['YOUTUBE_URL']
TIME_DELAY = fetcher_config['DEFAULT']['TIME_DELAY']
TOTAL_DURATION = fetcher_config['DEFAULT']['TOTAL_DURATION']
nb_iterations = int(float(TOTAL_DURATION)/float(TIME_DELAY))

print_log("LOG", f"Creating directory for {START_TIME} frame fetch run...")
os.mkdir(f"./model/data/raw_data/{START_TIME}")
print_log("OK", "Directory created successfully!")

print_log("LOG", f"Launching frame fetch run for {TOTAL_DURATION} seconds...")
for i in range(1, nb_iterations+1):
    current_frame = get_frame()
    try:
        cv2.imwrite(f"./model/data/raw_data/{START_TIME}/out{i}.png", current_frame)
        print_log("OK", f"Fetched and saved frame {i}.")
    except cv2.error:
        print_log("WARN", f"Could not fetch frame number {i}, moving on to next iteration...")
    sleep(float(TIME_DELAY))
print_log("OK", f"Finished {START_TIME} frame fetch run!")

print_log("WARN", "Remember to run \"dvc add\" to track newly added data files!")
