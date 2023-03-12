from fastapi import APIRouter

from api.v1.endpoints import visitation
from api.v1.endpoints import location
from api.v1.endpoints import person

api_router = APIRouter()
api_router.include_router(visitation.router, prefix='/visitation', tags=['visits'])
api_router.include_router(location.router, prefix='/location', tags=['locals'])
api_router.include_router(person.router, prefix='/person', tags=['persons'])
