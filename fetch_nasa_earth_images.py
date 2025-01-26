from helper_functions import saving_image
from environs import Env
from datetime import datetime
import requests
import argparse
import os


def receiving_earth_images_nasa(api_key, folder):
    os.makedirs(folder, exist_ok=True)
    metadata_url = f'https://api.nasa.gov/EPIC/api/natural/'
    params = {
        'api_key': api_key
    }

    response = requests.get(metadata_url, params=params)
    response.raise_for_status()

    images_name = list(name_image['image'] for name_image in response.json())
    images_date = response.json()[0]['date']
    images_date = datetime.strptime(images_date, "%Y-%m-%d %H:%M:%S")
    images_date = images_date.strftime("%Y/%m/%d")

    for img in images_name:
        image = f'{img}.png'
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{images_date}/png/{img}.png'

        params = {
            'api_key': api_key
        }
        saving_image(folder, image, image_url, params)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY')

    folder = os.path.join('photos from space', 'earth photos nasa')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default=folder, type=str)
    args = parser.parse_args()
    directory = args.directory

    try:
        receiving_earth_images_nasa(api_key, directory)
    except NotADirectoryError:
        print('В данной системе нельзя использовать слов "con" или символы "\/:*?"<>|" для создания папок или файлов!')
