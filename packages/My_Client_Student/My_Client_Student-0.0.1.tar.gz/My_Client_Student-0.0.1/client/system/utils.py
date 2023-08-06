"""Утилиты"""
from json import loads, dumps
from .config import MAXIMUM_MESSAGE_LENGTH, ENCODING


def get_message(user):
    """Функция приема сообщения"""
    encoded_response = user.recv(MAXIMUM_MESSAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(user, message):
    """Функция отправки сообщения"""
    if not isinstance(message, dict):
        raise TypeError
    message = dumps(message)
    encoded_message = message.encode(ENCODING)
    user.send(encoded_message)

