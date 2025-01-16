from helper_functions import saving_image
import argparse
import requests
import os


def get_spacex_images(images_id):
    if images_id:
        url = f'https://api.spacexdata.com/v5/launches/{images_id}'
        response = requests.get(url)
        response.raise_for_status()

        return response.json()['links']['flickr']['original']
    else:
        url = 'https://api.spacexdata.com/v5/launches'
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()

        for launche in reversed(launches):
            if launche['links']['flickr']['original']:
                return launche['links']['flickr']['original']


def creation_spacex_images(images):
    folder = f'photos from space/spacex'
    os.makedirs(folder, exist_ok=True)

    for image_number, url_image in enumerate(images):
        picture = f'spacex{image_number}.jpg'
        saving_image(folder, picture, url_image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('images_id', nargs='?', default='')
    args = parser.parse_args()
    user_images_id = args.images_id
    images = get_spacex_images(user_images_id)

    creation_spacex_images(images)


