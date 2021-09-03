from django.http import HttpResponseRedirect


def get_client_ip(request):
    """
    Get client ip address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    if 'HTTP_USER_AGENT' in request.META:
        return request.META['HTTP_USER_AGENT']
    return None


def redirect_back(request):
    """
        Redirect to HTTP_REFERER header from response
    """
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))
