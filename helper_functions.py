from urllib.parse import urlparse
import telegram
import requests
import time
import os


def get_file_type(url):
    file = urlparse(url).path
    file_type = os.path.splitext(file)[-1]

    return file_type


def calculation_in_seconds(timing):
    seconds_in_minute = timing * 60
    return seconds_in_minute


def sending_post(folder, image, bot, channel_id):
    image_path_post = os.path.join(folder, image)
    with open(image_path_post, 'rb') as picture_for_message:
        bot.send_document(chat_id=channel_id, document=picture_for_message)



def saving_image(folder, image, url, params=None):
    image_path = os.path.join(folder, image)
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(image_path, 'wb') as file:
        file.write(response.content)


def get_launches_data(images_id):
    url = f'https://api.spacexdata.com/v5/launches/{images_id}'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()
