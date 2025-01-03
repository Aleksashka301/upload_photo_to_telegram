from urllib.parse import urlparse
from environs import Env
import argparse
import requests
import os


def get_file_type(url):
    file = urlparse(url).path
    file_type = os.path.splitext(file)[-1]

    return file_type


def get_nasa_images(api_key, quantity_images):
    folder = f'photos from space/nasa'
    os.makedirs(folder, exist_ok=True)

    params = {
        'api_key': api_key,
        'count': quantity_images
    }

    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=params)
    response.raise_for_status()
    links_images = {}

    for obj in response.json():
        try:
            links_images[obj['title'].replace(' ', '_')] = obj['url']
        except KeyError:
            print('Ссылка не найдена!')
            continue

    for key, values in links_images.items():
        try:
            response = requests.get(values)
            response.raise_for_status()
        except requests.exceptions.MissingSchema:
            print(f'Не верная ссылка: {values}')
            continue

        for symbol in '\/:*?"<>|':
            key = key.replace(symbol, '')

        type_image = get_file_type(values)
        image = f'{key}{type_image}'
        image_path = os.path.join(folder, image)

        if values.find('apod.nasa.gov') != -1:
            with open(image_path, 'wb') as file:
                file.write(response.content)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY')

    parser = argparse.ArgumentParser()
    parser.add_argument('count', nargs='?', default=30, type=int)
    args = parser.parse_args()
    quantity_images = args.coint

    get_nasa_images(api_key, quantity_images)

