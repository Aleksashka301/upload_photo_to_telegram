from helper_functions import calculation_in_seconds, sending_post
from environs import Env
import argparse
import telegram
import random
import time
import sys
import os


def get_images_path(folder):
    folders_pictures = list(os.walk(folder))
    images_path = {}

    for _, objects in enumerate(folders_pictures, 1):
        directory, __, images = objects
        images_path[directory] = images

    return images_path


def post_to_telegram(images_path, chat_id, bot, image=None):
    if image:
        for key, values in images_path.items():
            if image in values:
                folder_images = key
                break
        try:
            sending_post(folder_images, image, bot, chat_id)
        except UnboundLocalError:
            print('Изображения с таким именем или форматом нет!')
    else:
        folder_images = random.choice(list(images_path.keys()))
        image_post = random.choice(images_path[folder_images])

        sending_post(folder_images, image_post, bot, chat_id)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    telegram_token = env.str('TELEGRAM_TOKEN')
    channel_id = env.str('TG_CHANNEL_ID')
    trigger_interval = env.int('TRIGGER_INTERVAL')
    bot = telegram.Bot(token=telegram_token)

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default='photos from space', type=str)
    parser.add_argument('time', nargs='?', type=int)
    parser.add_argument('image', nargs='?', type=str)
    args = parser.parse_args()
    directory = args.directory
    start_interval = args.time
    image_name = args.image

    try:
        images_path = get_images_path(directory)
        post_to_telegram(images_path, channel_id, bot, image_name)
    except IndexError:
        print('Выбранная директория не существует! Работа программы завершена!')
        sys.exit(1)

    while True:
        if not start_interval:
            time.sleep(trigger_interval)
        else:
            time.sleep(calculation_in_seconds(start_interval))

        folder_images = random.choice(list(images_path.keys()))
        image_post = random.choice(images_path[folder_images])

        try:
            sending_post(folder_images, image_post, bot, channel_id)
        except telegram.error.NetworkError:
            print('Соединение с интернетом разорвано, повторная отправка...')
            time.sleep(10)
