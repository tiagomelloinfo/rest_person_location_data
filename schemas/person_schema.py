from pydantic import Field
from pydantic import BaseModel as SCBaseModel

class PersonSchemaSave(SCBaseModel):
    name: str
    status: str
    species: str
    gender: str
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
