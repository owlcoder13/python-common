from django.http.request import HttpRequest
import threading
from typing import Union

GLOBAL_REQUEST_STORAGE = threading.local()


class GlobalRequestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        GLOBAL_REQUEST_STORAGE.request = request

        try:
            return self.get_response(request)
        finally:
            del GLOBAL_REQUEST_STORAGE.request


def get_request() -> Union[HttpRequest, None]:
    try:
        return GLOBAL_REQUEST_STORAGE.request

    except AttributeError:
        request = HttpRequest()
        request.path = '/'
        request.META['HTTP_HOST'] = 'localhost:8000'
        return request
