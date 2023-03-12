from pydantic import BaseModel as SCBaseModel
from pydantic import Field

from typing import Literal

class PersonSchemaSave(SCBaseModel):
    name: str
    status: Literal['Alive', 'Dead', 'unknown']
    species: str
    gender: Literal['Female', 'Male', 'Genderless', 'unknown']
    origin: str

class PersonSchemaReturn(SCBaseModel):
    id: int
    name: str
    status: str
    species: str
    gender: str
    origin: object
    location: list | None
    url: str
    created: str

    class Config:
        orm_mode = True
