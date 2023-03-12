from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.location_model import Location

from schemas.location_schema import LocalSchemaRequest
from schemas.location_schema import LocalSchemaResponse

from api.v1.endpoints.visitation import get_visit_local

from core.deps import get_session
from core.config import settings

router = APIRouter()

# POST Local
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LocalSchemaResponse)
async def post_local(local: LocalSchemaRequest, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(Location).filter(Location.name == local.name.title().strip())
        result = await session.execute(query)
        consulta = result.scalar_one_or_none()

        if not consulta:
            new_local = Location(
                name = local.name.title().strip(),
                dimension = local.dimension.title().strip(),
                created = str(datetime.now())
            )

            db.add(new_local)
            await db.commit()

            new_local.url = f'{settings.URI_BASE}/api/v1/location/{new_local.id}'
            res = new_local
        else:
            consulta.url = f'{settings.URI_BASE}/api/v1/location/{consulta.id}'
            res = consulta

        return res

# GET Locals
@router.get('/', response_model=List[LocalSchemaResponse])
async def get_locations(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Location)
        result = await session.execute(query)
        local_list: List[Location] = result.scalars().all()

        for local in local_list:
            local.residents = await get_visit_local(local_id = local.id, db = db)
            local.url = f'{settings.URI_BASE}/api/v1/location/{local.id}'

        return local_list

# GET Local
@router.get('/{local_id}', response_model=LocalSchemaResponse, status_code=status.HTTP_200_OK)
async def get_local(local_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Location).filter(Location.id == local_id)
        result = await session.execute(query)
        local = result.scalar_one_or_none()

        if local:
            local.residents = await get_visit_local(local_id = local_id, db = db)
            local.url = f'{settings.URI_BASE}/api/v1/location/{local.id}'
            return local
        else:
            raise HTTPException(detail='Local não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# PUT Location
@router.put('/{local_id}', response_model=LocalSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_local(local_id: int, local: LocalSchemaRequest, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Location).filter(Location.id == local_id)
        result = await session.execute(query)
        local_up = result.scalar_one_or_none()

        if local_up:
            local_up.name = local.name.title().strip()
            local_up.dimension = local.dimension.title().strip()
            await session.commit()

            local_up.url = f'{settings.URI_BASE}/api/v1/location/{local_up.id}'
            local_up.residents = await get_visit_local(local_id = local_id, db = db)
            return local_up
        else:
            raise HTTPException(detail='Local não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Local
@router.delete('/{local_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_local(local_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Location).filter(Location.id == local_id)
        result = await session.execute(query)
        local_del = result.scalar_one_or_none()

        if local_del:
            await session.delete(local_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Local não encontrado', status_code=status.HTTP_404_NOT_FOUND)
