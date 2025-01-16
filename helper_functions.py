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
    path_image_post = os.path.join(folder, image)
    try:
        with open(path_image_post, 'rb') as picture_for_message:
            bot.send_document(chat_id=channel_id, document=picture_for_message)
    except telegram.error.NetworkError:
        print('Соединение с интернетом разорвано, повторная отправка...')
        time.sleep(10)


def saving_image(folder, image, url, params={}):
    image_path = os.path.join(folder, image)
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(image_path, 'wb') as file:
        file.write(response.content)
