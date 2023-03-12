from typing import List

from datetime import datetime

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.visitation_model import VisitationModel
from models.location_model import Location
from models.person_model import Person

from schemas.visitation_schema import VisitationRequest
from schemas.visitation_schema import VisitationResponse
from schemas.visitation_schema import VisitationLocalResponse
from schemas.visitation_schema import VisitationPersonResponse

from core.deps import get_session
from core.config import settings

router = APIRouter()

# Post Visit
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=VisitationResponse)
async def post_visitation(visitation: VisitationRequest, db: AsyncSession = Depends(get_session)):

    async with db as session:
        new_visitation = VisitationModel(
            person_id = visitation.person_id,
            location_id = visitation.location_id,
            created = str(datetime.now())
        )

        res = {}

        try:
            query = select(Location).filter(Location.id == visitation.location_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()
            res['location_name'] = temp.name
            res['location_url'] = f'{settings.URI_BASE}/api/v1/location/{temp.id}'

            query = select(Person).filter(Person.id == visitation.person_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()
            res['person_name'] = temp.name
            res['person_url'] = f'{settings.URI_BASE}/api/v1/person/{temp.id}'

            res['created'] = new_visitation.created

            db.add(new_visitation)
            await db.commit()
            
            return res
        except:
            raise HTTPException(detail='Person or Location not found', status_code=status.HTTP_404_NOT_FOUND)

# GET Locals
@router.get('/', response_model=List[VisitationResponse])
async def get_visit(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VisitationModel)
        result = await session.execute(query)
        visitation_list: List[VisitationModel] = result.scalars().all()

        lista: List[Location] = []
        for visitation in visitation_list:
            res = {}

            query = select(Location).filter(Location.id == visitation.location_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()
            res['location_name'] = temp.name
            res['location_url'] = f'{settings.URI_BASE}/api/v1/location/{temp.id}'

            query = select(Person).filter(Person.id == visitation.person_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()
            res['person_name'] = temp.name
            res['person_url'] = f'{settings.URI_BASE}/api/v1/person/{temp.id}'

            res['created'] = visitation.created

            lista.append(res)

        return lista

# GET by Local id
async def get_visit_local(local_id: int, db: AsyncSession = Depends(get_session)) -> list:
    async with db as session:
        query = select(VisitationModel).filter(VisitationModel.location_id == local_id)
        result = await session.execute(query)
        visitation_list: List[VisitationModel] = result.scalars().all()

        lista: List[Person] = []
        for visitation in visitation_list:
            res = {}

            query = select(Person).filter(Person.id == visitation.person_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()

            if temp:
                res['person_name'] = temp.name
                res['person_url'] = f'{settings.URI_BASE}/api/v1/person/{temp.id}'

            if not res in lista:
                lista.append(res)

        return lista

# Get person by id
async def get_visit_person(person_id: int, db: AsyncSession = Depends(get_session)) -> list:
    async with db as session:
        query = select(VisitationModel).filter(VisitationModel.person_id == person_id)
        result = await session.execute(query)
        visitation_list: List[VisitationModel] = result.scalars().all()

        lista: List[Location] = []
        for visitation in visitation_list:
            res = {}

            query = select(Location).filter(Location.id == visitation.location_id)
            result = await session.execute(query)
            temp = result.scalar_one_or_none()

            if temp:
                res['location_name'] = temp.name
                res['location_url'] = f'{settings.URI_BASE}/api/v1/location/{temp.id}'

            if not res in lista:
                lista.append(res)

        return lista

async def get_origin_location(origin: str, db: AsyncSession = Depends(get_session)) -> dict:
    async with db as session:
        query = select(Location).filter(Location.name == origin)
        result = await session.execute(query)
        visitation = result.scalar_one_or_none()

        if visitation:
            res = {
                'name': visitation.name,
                'url': f'{settings.URI_BASE}/api/v1/location/{visitation.id}'
            }
        else:
            res = {
                'name': origin,
                'url': None
            }

        return res
