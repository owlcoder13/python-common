import os
from django.conf import settings


def get_file_contents(path):
    """
    Similar to php get_file_contents
    """
    with open(os.path.join(settings.BASE_DIR, path), 'r', encoding='utf-8') as f:
        out = f.read()
        return out
