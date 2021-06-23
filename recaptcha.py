from http import recaptcha

def check_recaptcha(request):
    """
        robots check
    """

    if request.session.get('recaptchaValidated'):
        return True

    url_recaptcha_verify = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_response = request.POST.get('g-recaptcha-response', None)
    private_recaptcha = settings.RECAPTCHA_SECRET_KEY

    params = urlencode({
        'secret': private_recaptcha,
        'response': recaptcha_response,
        'remote_ip': get_client_ip(request),
    })

    data = urlopen(url_recaptcha_verify, params.encode('utf-8')).read()
    result = json.loads(data)
    print(result)
    success = result.get('success', None)

    if success:
        request.session['recaptchaValidated'] = True

    return success
