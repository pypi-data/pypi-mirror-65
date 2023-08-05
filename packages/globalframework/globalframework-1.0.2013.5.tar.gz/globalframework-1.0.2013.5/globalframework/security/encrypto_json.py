import json
from kombu.serialization import register

from globalframework.data.setting import QueueSetting
from globalframework.security.encrypto import Crypto

fernet = Crypto()
settings = QueueSetting().get_queue_connection()

MIMETYPE = 'application/x-fernet-json'


def fernet_encode(func):
    def inner(message):
        message = func(message)
        return fernet.encrypt(message, settings['CELERY_KEY'])
    return inner


def fernet_decode(func):
    def inner(encoded_message):
        if isinstance(encoded_message, str):
            encoded_message = encoded_message.encode('utf-8')
        message = fernet.decrypt(encoded_message, settings['CELERY_KEY'])
        return func(message)
    return inner


register(
    'fernet_json',
    fernet_encode(json.dumps),
    fernet_decode(json.loads),
    MIMETYPE,
    'utf-8'
)
