from helper_functions import get_file_type, saving_image
from environs import Env
import argparse
import requests
import os


def get_nasa_images(api_key, quantity_images):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': quantity_images
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    links_images = {}

    for obj in response.json():
        try:
            title = obj['title'].replace(' ', '_').replace('\r', '').replace('\n', '').strip()
            links_images[title] = obj['url']
        except KeyError:
            print('Ссылка не найдена!')
            continue

    return links_images


def download_nasa_images(api_key, quantity_images):
    folder = f'photos from space/nasa'
    os.makedirs(folder, exist_ok=True)
    links_images = get_nasa_images(api_key, quantity_images)

    for key, values in links_images.items():
        for symbol in '\/:*?"<>|':
            key = key.replace(symbol, '')

        type_image = get_file_type(values)
        image = f'{key}{type_image}'

        try:
            saving_image(folder, image, values)
        except (requests.exceptions.MissingSchema, requests.exceptions.HTTPError) as error:
            print(f'Не верная ссылка: {error}')
            continue


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY')

    parser = argparse.ArgumentParser()
    parser.add_argument('count', nargs='?', default=30, type=int)
    args = parser.parse_args()
    quantity_images = args.count

    download_nasa_images(api_key, quantity_images)

