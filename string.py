import re
from io import StringIO
from html.parser import HTMLParser


class TagStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def is_email(email):
    regex = r'[^@]+@[^@]+\.[^@]+'
    return re.match(regex, email)


def truncate_chars(text, cnt=50):
    if len(text) > cnt:
        text = text[0:cnt].strip() + '...'

    return text


def strip_tags(text):
    s = TagStripper()
    s.feed(text)
    return s.get_data()
