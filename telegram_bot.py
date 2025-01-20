from helper_functions import calculation_in_seconds, sending_post
from environs import Env
import argparse
import telegram
import random
import time
import os


def post_to_telegram_and_get_next(chat_id, bot, image=None):
    folders_pictures = list(os.walk('photos from space'))
    path_images = {}

    for folder, objects in enumerate(folders_pictures):
        if folder == 0:
            continue
        path_images[objects[0]] = objects[2]

    if image:
        for key, values in path_images.items():
            if image in values:
                folder_images = key
                break
        try:
            sending_post(folder_images, image, bot, chat_id)
        except UnboundLocalError:
            print('Изображения с таким именем или форматом нет!')
    else:
        folder_images = random.choice(list(path_images.keys()))
        image_post = random.choice(path_images[folder_images])

        sending_post(folder_images, image_post, bot, chat_id)

    return path_images


if __name__ == '__main__':
    env = Env()
    env.read_env()
    telegram_token = env.str('TELEGRAM_TOKEN')
    channel_id = env.str('TG_CHANNEL_ID')
    trigger_interval = env.int('TRIGGER_INTERVAL')
    bot = telegram.Bot(token=telegram_token)

    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='?', type=int)
    parser.add_argument('image', nargs='?', type=str)
    args = parser.parse_args()
    start_interval = args.time
    name_image = args.image

    path_images = post_to_telegram_and_get_next(channel_id, bot, name_image)

    while True:
        if not start_interval:
            time.sleep(trigger_interval)
        else:
            time.sleep(calculation_in_seconds(start_interval))

        folder_images = random.choice(list(path_images.keys()))
        image_post = random.choice(path_images[folder_images])

        try:
            sending_post(folder_images, image_post, bot, channel_id)
        except telegram.error.NetworkError:
            print('Соединение с интернетом разорвано, повторная отправка...')
            time.sleep(10)