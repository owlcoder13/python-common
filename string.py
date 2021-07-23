import re


def is_email(email):
    regex = r'[^@]+@[^@]+\.[^@]+'
    return re.match(regex, email)
