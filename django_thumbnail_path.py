"""
For this library please specify path to empty image in settings: EMPTY_IMAGE_URL=... like BASE_PATh/main/static/no-image.png (not exists)
"""
from django import template
from django.conf import settings
from PIL import Image, ImageOps
import os

register = template.Library()


def empty_image_path():
    return settings.EMPTY_IMAGE_PATH


def resize(source, destination, width, height):
    """
    Resize image from source path and saves it to destination path by width and height
    :param source:
    :param destination:
    :param width:
    :param height:
    :return:
    """
    img = Image.open(source)
    img = img.copy()
    img = ImageOps.fit(img, (width, height), Image.ANTIALIAS)
    img.save(destination)


def no_image(width, height):
    """
    :param width: width of no image
    :param height: height of no image
    :return: path of new image with specified sizes
    """
    path_to_empty_image = empty_image_path()
    image_name = 'no-image.png'
    empty_name = '%s_%s_%s' % (width, height, image_name)
    save_path = os.path.join(settings.STATIC_ROOT, empty_name)
    if not os.path.exists(save_path):
        resize(path_to_empty_image,
               save_path, width, height)
    uri = os.path.join(settings.STATIC_URL, empty_name)
    return uri


def thumbnail_uri(path, width, height, override=False):
    """
    todo: Доделать метод. Пока не работает
    Сохраняет картинку из любого uri(обычно находится в uploads) проекта на <uri to image>/thumbnails/
    """
    basedir = os.path.dirname(path)
    save_directory = os.path.join(basedir, 'thumbnails')
    return get_media_uri_thumbnail(save_directory, path, width, height, override)


def thumbnail_path(path, width, height, override=False):
    """
    Сохраняет картинку из любого пути проекта на uploads/static
    """
    if not os.path.exists(path):
        return no_image(width, height)

    save_directory = os.path.join(settings.MEDIA_ROOT, 'static')
    return get_media_uri_thumbnail(save_directory, path, width, height, override)


def get_media_uri_thumbnail(save_dir, path, width, height, override=False):
    filename = os.path.basename(path)
    th_filename = '%s_%s_%s' % (width, height, filename)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    th_full_path = os.path.join(save_dir, th_filename)

    if override or not os.path.exists(th_full_path):
        resize(path, th_full_path, width, height)

    return settings.MEDIA_URL + th_full_path[len(settings.MEDIA_ROOT) + 1:]
