from pydantic import Field
from pydantic import BaseModel as SCBaseModel

class LocalSchemaRequest(SCBaseModel):
    name: str = Field(example = "Earth")
    dimension: str = Field(example = "001")

class LocalSchemaResponse(SCBaseModel):
    id: int = Field(example = 1)
    name: str = Field(example = "Earth")
    dimension: str = Field(example = "001")
    residents: list | None = Field(example = [{"name": "Person1", "url": "api/v1/person/1"}])
    url: str = Field(example = "api/v1/person/1")
    created: str = Field(example = "/api/v1/location/5")

    class Config:
        orm_mode = True
