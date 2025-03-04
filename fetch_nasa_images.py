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
    images_links = {}

    for obj in response.json():
        try:
            title = obj['title'].replace(' ', '_').replace('\r', '').replace('\n', '').strip()
            images_links[title] = obj['url']
        except KeyError:
            print('Ссылка не найдена!')
            continue

    return images_links


def download_nasa_images(api_key, quantity_images, folder):
    os.makedirs(folder, exist_ok=True)
    images_links = get_nasa_images(api_key, quantity_images)

    for key, values in images_links.items():
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

    folder = os.path.join('photos from space', 'nasa')
    parser = argparse.ArgumentParser()
    parser.add_argument('count', nargs='?', default=30, type=int)
    parser.add_argument('directory', nargs='?', default=folder, type=str)
    args = parser.parse_args()
    images_quantity = args.count
    directory = args.directory

    try:
        download_nasa_images(api_key, images_quantity, directory)
    except NotADirectoryError:
        print('В данной системе нельзя использовать слов "con" или символы "\/:*?"<>|" для создания папок или файлов!')

