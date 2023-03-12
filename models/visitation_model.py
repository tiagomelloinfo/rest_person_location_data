from core.config import settings

from sqlalchemy import Column, Integer, String

class VisitationModel(settings.DBBaseModel):
    __tablename__ = 'visitation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer)
    location_id = Column(Integer)
    created = Column(String)
