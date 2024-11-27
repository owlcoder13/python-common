from captcha.image import ImageCaptcha
from django.http import JsonResponse
import base64
from pprint import pprint 
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

crypto_key = b'jQhGzdRnbMLv-5MwrVw454uDj2XB966EGU9j8mwEtC4='

def encrypt_code(code):
    '''
        Шифруем код, чтобы записать в куки
    '''
    f = Fernet(crypto_key)
    bytes_string = bytes(code, 'utf-8')
    return f.encrypt(bytes_string).decode('utf-8')

def decrypt_code(encrypted_code):
    '''
        Дешифруем код, чтобы записать в куки
    '''
    try:
        f = Fernet(crypto_key)
        bytes_string = bytes(encrypted_code, 'utf-8')
        return f.decrypt(bytes_string).decode('utf-8')
    except Exception as e:
        return None

def get_image(code):
    '''
        Получение base64 кода картинки с указанным кодом
    '''

    font_path = os.path.join(settings.BASE_DIR, "common/captcha.ttf")
    print('font path', font_path)

    image = ImageCaptcha(fonts=[
        font_path
    ])
    bts = image.generate(code).getvalue()
    return base64.b64encode(bts).decode('utf-8')

def get_code_from_cookie(request):
    unique_id = request.COOKIES['captcha'] if 'captcha' in request.COOKIES else None

    if unique_id is not None:
        unique_id = decrypt_code(unique_id)
        return unique_id

    return None

def get_response_from_cookie(request):
    return request.COOKIES['captcha_response'] if 'captcha_response' in request.COOKIES else None
    

def check_captcha_from_request(request):
    
    if 'hide_captcha' in request.COOKIES:
        return True
    
    request_code = get_code_from_cookie(request)
    response_code = get_response_from_cookie(request)

    return request_code is not None and request_code == response_code

def view_get_image(request):
    '''
        Представление которое возвращает json с картинкой в base64
    '''
    unique_id = get_code_from_cookie(request)

    if unique_id is None or 'new' in request.GET:
        unique_id = get_random_string(length=4).lower()

    response = JsonResponse({'image': get_image(unique_id)})
    response.set_cookie('captcha', encrypt_code(unique_id))

    return response

def view_filled(request):
    return JsonResponse({
        "success": check_captcha_from_request(request),
    })

@csrf_exempt
def view_check_captcha(request):
    '''
        Представление должно записывать ответ капчи от пользователя чтобы позже его сравнивать
    '''
    unique_id = get_code_from_cookie(request)
    input_code = request.POST['code'].lower()

    success = False

    if unique_id == input_code:
        success = True

    response = JsonResponse({'success': success})
    response.set_cookie('captcha_response', input_code)

    return response

def check_captcha(request):
    '''
        Метод для проверки капчи для пользователя
    '''
    unique_id = request.COOKIES['captcha'] if 'captcha' in request.COOKIES else None

    if unique_id is None:
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})