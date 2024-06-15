import base64
import hmac
import json
from hashlib import sha256
from datetime import datetime
from django.conf import settings
import random
import string
from django.core.cache import cache


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def base64url_decode(data):
    padding = 4 - (len(data) % 4)
    return base64.urlsafe_b64decode(data + '=' * padding)


def create_jwt_token(user_id):
    header = {
        'alg': settings.JWT_SETTINGS['ALGORITHM'],
        'typ': 'JWT'
    }
    payload = {
        'user_id': user_id,
        'exp': (datetime.utcnow() + settings.JWT_SETTINGS['ACCESS_TOKEN_LIFETIME']).timestamp(),
        'iat': datetime.utcnow().timestamp()
    }

    header_encoded = base64url_encode(json.dumps(header).encode('utf-8'))
    payload_encoded = base64url_encode(json.dumps(payload).encode('utf-8'))

    signature = hmac.new(
        settings.JWT_SETTINGS['SIGNING_KEY'].encode('utf-8'),
        f'{header_encoded}.{payload_encoded}'.encode('utf-8'),
        sha256
    ).digest()

    signature_encoded = base64url_encode(signature)

    return f'{header_encoded}.{payload_encoded}.{signature_encoded}'


def verify_jwt_token(token):
    try:
        header_encoded, payload_encoded, signature_encoded = token.split('.')
        signature_check = hmac.new(
            settings.JWT_SETTINGS['SIGNING_KEY'].encode('utf-8'),
            f'{header_encoded}.{payload_encoded}'.encode('utf-8'),
            sha256
        ).digest()

        if base64url_encode(signature_check) != signature_encoded:
            return False

        payload = json.loads(base64url_decode(payload_encoded).decode('utf-8'))

        if datetime.utcnow().timestamp() > payload['exp']:
            return None

        return payload
    except Exception as e:
        return False


def number_generator(size=10):
    chars = string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def check_captcha_code(attrs):
    key_unique_id = attrs["key_unique_id"]
    obj = cache.get(key_unique_id)
    if obj:
        if obj == attrs["value_unique_id"]:
            cache.delete(key_unique_id)
            return True
        else:
            return False, {"message": "Your entered captcha is incorrect."}
    else:
        raise False, {"message": "Your captcha was expired."}
