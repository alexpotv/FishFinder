# Frame Fetcher Tool

The frame fetcher tool is meant to be used for raw data collection. When running the script, the collected frames are
saved into a new timestamped directory, in the following path:

`./model/data/raw_data`

## Dependencies

The following dependencies must be installed on the local system:
- [**FFMPEG**](https://ffmpeg.org)
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

To use the frame fetcher tool, simply run the associated Python script (`frame_fetcher.py`).
