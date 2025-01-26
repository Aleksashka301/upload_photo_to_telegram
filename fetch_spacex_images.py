from helper_functions import saving_image, get_launches_data
import argparse
import requests
import os


def get_launch_images_by_id(images_id=None):
    if images_id:
        try:
            launch = get_launches_data(images_id)
            return launch['links']['flickr']['original']
        except requests.exceptions.HTTPError:
            print(f'Запуска с таким id: {images_id} нет!')
            return get_launch_images()
    else:
        return get_launch_images()


def get_launch_images():
    images_id = ''
    launches = get_launches_data(images_id)

    for launch in reversed(launches):
        if launch['links']['flickr']['original']:
            return launch['links']['flickr']['original']


def creation_spacex_images(images, folder):
    os.makedirs(folder, exist_ok=True)

    for image_number, url_image in enumerate(images):
        picture = f'spacex{image_number}.jpg'
        saving_image(folder, picture, url_image)


if __name__ == '__main__':
    folder = os.path.join('photos from space', 'spacex')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default=folder, type=str)
    parser.add_argument('images_id', nargs='?', default='')
    args = parser.parse_args()
    directory = args.directory
    user_images_id = args.images_id

    try:
        images = get_launch_images_by_id(user_images_id)
        creation_spacex_images(images, directory)
    except NotADirectoryError:
        print('В данной системе нельзя использовать слов "con" или символы "\/:*?"<>|" для создания папок или файлов!')
