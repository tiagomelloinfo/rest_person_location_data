from core.config import settings

from sqlalchemy import Column, Integer, String

class Person(settings.DBBaseModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    status = Column(String)
    species = Column(String) 
    gender = Column(String)
    origin = Column(String)
    created = Column(String)
