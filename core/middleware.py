import json

from fastapi import Request

from core.config import settings
# from utils.telebot import Telebot

def autenticador(request: Request):
    endpoint = str(request.url).split('/')[3]

    # telebot = Telebot()
    # msg = json.dumps({'auth_res': auth_res,'endpoint_access': endpoint, 'user': user})
    # telebot.enviar(log_type='auth', msg=msg)

    if endpoint in settings.endpoints_permitidos:
        return True
    else:
        return request.headers.get('token', '') == settings.TOKEN
    