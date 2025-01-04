from urllib.parse import urlparse
import os


def get_file_type(url):
    file = urlparse(url).path
    file_type = os.path.splitext(file)[-1]

    return file_type


def time_interval(timing):
    seconds_in_minute = timing * 60
    return seconds_in_minute
