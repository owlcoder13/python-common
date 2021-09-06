import os
from django.conf import settings
from slugify import slugify
from django.utils.crypto import get_random_string


def get_file_contents(path):
    """
    Similar to php get_file_contents
    It reads full file and return it's content
    """
    with open(os.path.join(settings.BASE_DIR, path), 'r', encoding='utf-8') as f:
        out = f.read()
        return out


def save_file_unique_slugify(directory, filename):
    """
    Helper for save files in django in some directory
    This function slugify file name, create directory and
    make file name unique with random suffix
    """

    def make_full_path(path):
        return os.path.join(settings.BASE_DIR, directory, path)

    full_directory_path = os.path.join(settings.BASE_DIR, directory)

    if not os.path.exists(full_directory_path):
        os.makedirs(full_directory_path)

    f_name, _dot, extension = filename.rpartition('.')
    slug = slugify(f_name)

    new_file_name = "%s.%s" % (slug, extension)

    while os.path.exists(make_full_path(new_file_name)):
        new_file_name = "%s-%s.%s" % (slug, get_random_string(8), extension)

    return os.path.join(directory, new_file_name)
