from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

from decouple import config

class Settings(BaseSettings):
    '''
    Configurações gerais usadas na aplicação
    '''
    API_V1_STR = '/api/v1'
    TOKEN = config('TOKEN')
    DB_URL = config('DB_URL') if config('DB_URL') else 'sqlite+aiosqlite:///database'
    URI_BASE = config('URI_BASE') if config('URI_BASE') else 'http://localhost:8000'
    DBBaseModel = declarative_base()

    endpoints_permitidos = ('docs', 'redoc', 'openapi.json', 'pesquisar')

    class Config:
        case_sensitive = True

settings = Settings()
