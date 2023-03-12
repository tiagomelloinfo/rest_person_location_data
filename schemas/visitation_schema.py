from pydantic import BaseModel as SCBaseModel
from pydantic import Field

class VisitationRequest(SCBaseModel):
    person_id: int
    location_id: int

class VisitationResponse(SCBaseModel):
    person_name: str
    person_url: str
    location_name: str
    location_url: str
    created: str

    class Config:
        orm_mode = True

class VisitationLocalResponse(SCBaseModel):
    location_name: str
    location_url: str

class VisitationPersonResponse(SCBaseModel):
    person_name: str
    person_url: str
