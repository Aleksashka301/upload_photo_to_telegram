import argparse
import requests
import os


def fetch_spacex_last_launch(images_id):
    folder = f'photos from space/spacex'
    os.makedirs(folder, exist_ok=True)

    if images_id:
        url = f'https://api.spacexdata.com/v5/launches/{images_id}'
        response = requests.get(url)
        response.raise_for_status()
        images = response.json()['links']['flickr']['original']
    else:
        url = 'https://api.spacexdata.com/v5/launches'
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()

        for launche in reversed(launches):
            if launche['links']['flickr']['original']:
                images = launche['links']['flickr']['original']
                break

    for image_number, url_image in enumerate(images):
        response = requests.get(url_image)
        response.raise_for_status()

        picture = f'spacex{image_number}.jpg'
        image_path = os.path.join(folder, picture)

        with open(image_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('images_id', nargs='?', default='')
    args = parser.parse_args()
    user_images_id = args.images_id

    fetch_spacex_last_launch(user_images_id)
