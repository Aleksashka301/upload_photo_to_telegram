from environs import Env
import requests
import os


def receiving_earth_images_nasa(api_key):
    folder = f'photos from space/earth photos nasa'
    os.makedirs(folder, exist_ok=True)

    url_metadata = f'https://api.nasa.gov/EPIC/api/natural?api_key={api_key}'
    response = requests.get(url_metadata)
    response.raise_for_status()

    name_images = list(name_image['image'] for name_image in response.json())
    date_images = response.json()[0]['date'].split()[0].replace('-', '/')

    for img in name_images:
        url_image = f'https://api.nasa.gov/EPIC/archive/natural/{date_images}/png/{img}.png'
        params = {
            'api_key': api_key
        }
        response = requests.get(url_image, params=params)
        response.raise_for_status()

        image = f'{img}.png'
        image_path = os.path.join(folder, image)

        with open(image_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY')

    receiving_earth_images_nasa(api_key)
