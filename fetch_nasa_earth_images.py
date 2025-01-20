from helper_functions import saving_image
from environs import Env
from datetime import datetime
import requests
import os


def receiving_earth_images_nasa(api_key):
    folder = os.path.join('photos from space', 'earth photos nasa')
    os.makedirs(folder, exist_ok=True)

    url_metadata = f'https://api.nasa.gov/EPIC/api/natural/'
    params = {
        'api_key': api_key
    }
    response = requests.get(url_metadata, params=params)
    response.raise_for_status()

    name_images = list(name_image['image'] for name_image in response.json())
    date_images = response.json()[0]['date']
    date_images = datetime.strptime(date_images, "%Y-%m-%d %H:%M:%S")
    date_images = date_images.strftime("%Y/%m/%d")

    for img in name_images:
        image = f'{img}.png'
        url_image = f'https://api.nasa.gov/EPIC/archive/natural/{date_images}/png/{img}.png'

        params = {
            'api_key': api_key
        }
        saving_image(folder, image, url_image, params)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY')

    receiving_earth_images_nasa(api_key)
