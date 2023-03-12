from core.config import settings

from sqlalchemy import Column, Integer, String

class Location(settings.DBBaseModel):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    dimension = Column(String) 
    created = Column(String)
