from helper_functions import saving_image, get_launches_data
import argparse
import os


def get_spacex_images(images_id=None):
    if images_id:
        launch = get_launches_data(images_id)
        return launch['links']['flickr']['original']
    else:
        images_id = ''
        launches = get_launches_data(images_id)

        for launch in reversed(launches):
            if launch['links']['flickr']['original']:
                return launch['links']['flickr']['original']


def creation_spacex_images(images):
    folder = os.path.join('photos from space', 'spacex')
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


