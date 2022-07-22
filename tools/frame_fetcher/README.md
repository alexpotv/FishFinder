# Data Collection Tool

The data collection tool is meant to be used for raw data collection. When running the script, the collected frames are
saved into a new timestamped directory, in the following path:

`./model/data/raw_data`

## Dependencies

In addition to the project requirements (which are specified in the `requirements.txt` file), the following dependencies 
must also be installed on the local system:

- [**YouTube-DL**](https://youtube-dl.org)

## Configuration file

The configuration file (`FETCHER_CONFIG.ini`) contains the following configuration values:
- **YOUTUBE_URL**: The YouTube live stream URL to fetch frames from
- **TIME_DELAY**: The delay (in seconds) between each frame being fetched
- **TOTAL_DURATION**: The total duration of the frame-fetching session

> ⚠️ **Important**
> 
> When setting the **live-stream URL** configuration value, **any "%" character must be padded with another "%" 
> character**. This is due to the interpolation functionality of the native Python `configparse` library.

## Usage

To use the data collection tool, simply run the associated Python script (`frame_fetcher.py`).

## Frame Fetcher Module

The `frame_fetcher.py` file contains the Python script which fetches the frame from the live-stream. The `get_frame` 
function might also be used elsewhere in the project, where fetching a frame from the live stream is needed.
