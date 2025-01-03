from environs import Env
import argparse
import telegram
import random
import time
import os


def post_to_telegram_and_get_next(image=''):
    folders_pictures = list(os.walk('photos from space'))
    path_images = {}

    for path in folders_pictures[1:]:
        path_images[path[0]] = path[2]

    if image:
        for key, values in path_images.items():
            if image in values:
                folder_images = key
                break

        path_image_post = f'{folder_images}/{image}'
        bot.send_document(chat_id=chat_id, document=open(path_image_post, 'rb'))
    else:
        folder_images = random.choice(list(path_images.keys()))
        image_post = random.choice(path_images[folder_images])
        path_image_post = f'{folder_images}/{image_post}'
        bot.send_document(chat_id=chat_id, document=open(path_image_post, 'rb'))

    return path_images


def time_interval(timing):
    seconds_in_minute = timing * 60
    return seconds_in_minute


if __name__ == '__main__':
    env = Env()
    env.read_env()
    telegram_token = env.str('TELEGRAM_TOKEN')
    chat_id = env.str('CHAT_ID')
    trigger_interval = env.int('TRIGGER_INTERVAL')
    bot = telegram.Bot(token=telegram_token)

    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='?', type=int)
    parser.add_argument('image', nargs='?', type=str)
    args = parser.parse_args()
    start_interval = args.time
    name_image = args.image

    path_images = post_to_telegram_and_get_next()
    path_images(name_image)

    while True:
        if not start_interval:
            time.sleep(trigger_interval)
        else:
            time.sleep(time_interval(start_interval))

        folder_images = random.choice(list(path_images.keys()))
        image_post = random.choice(path_images[folder_images])
        path_image_post = f'{folder_images}/{image_post}'

        bot.send_document(chat_id=chat_id, document=open(path_image_post, 'rb'))






