
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.location_model import Location

class Validate:
    def person_schema(self, status: str, gender: str):
        lista = []
        status_list = ('Alive', 'Dead', 'Unknown')
        gender_list = ('Female', 'Male', 'Genderless' , 'Unknown')

        if status.title() not in status_list:
            lista.append(status)
        if gender.title() not in gender_list:
            lista.append(gender)

        


validate = Validate()
