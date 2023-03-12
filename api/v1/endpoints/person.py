from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.person_model import Person

from schemas.person_schema import PersonSchemaSave
from schemas.person_schema import PersonSchemaReturn

from api.v1.endpoints.visitation import get_visit_person
from api.v1.endpoints.visitation import get_origin_location

from core.deps import get_session
from core.config import settings

router = APIRouter()

# POST Person
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PersonSchemaReturn)
async def post_person(person: PersonSchemaSave, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Person).filter(Person.name == person.name.title().strip())
        result = await session.execute(query)
        consulta = result.scalar_one_or_none()

        if not consulta:
            new_person = Person(
                name = person.name.title().strip(),
                status = person.status.title().strip(),
                species = person.species.title().strip(),
                gender = person.gender.title().strip(),
                origin = person.origin.title().strip(),
                created = str(datetime.now())
            )

            db.add(new_person)
            await db.commit()

            new_person.url = f'{settings.URI_BASE}/api/v1/person/{new_person.id}'
            new_person.origin = await get_origin_location(origin = new_person.origin, db = db)
            new_person.location = await get_visit_person(person_id = new_person.id, db = db)
            res = new_person
        else:
            consulta.url = f'{settings.URI_BASE}/api/v1/person/{consulta.id}'
            consulta.origin = await get_origin_location(origin = consulta.origin, db = db)
            consulta.location = await get_visit_person(person_id = consulta.id, db = db)
            res = consulta

        return res


# GET Persons
@router.get('/', response_model=List[PersonSchemaReturn])
async def get_persons(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Person)
        result = await session.execute(query)
        person_list: List[Person] = result.scalars().all()

        for person in person_list:
            person.origin = await get_origin_location(origin = person.origin, db = db)
            person.location = await get_visit_person(person_id = person.id, db = db)
            person.url = f'{settings.URI_BASE}/api/v1/person/{person.id}'

        return person_list

# GET Person by id
@router.get('/{person_id}', response_model=PersonSchemaReturn, status_code=status.HTTP_200_OK)
async def get_local(person_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Person).filter(Person.id == person_id)
        result = await session.execute(query)
        person = result.scalar_one_or_none()

        if person:
            person.origin = await get_origin_location(origin = person.origin, db = db)
            person.location = await get_visit_person(person_id = person.id, db = db)
            person.url = f'{settings.URI_BASE}/api/v1/person/{person.id}'
            return person
        else:
            raise HTTPException(detail='Person não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# PUT Person
@router.put('/{person_id}', response_model=PersonSchemaReturn, status_code=status.HTTP_202_ACCEPTED)
async def put_local(person_id: int, person: PersonSchemaSave, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Person).filter(Person.id == person_id)
        result = await session.execute(query)
        person_up = result.scalar_one_or_none()

        if person_up:
            person_up.name = person.name.title().strip()
            person_up.status = person.status.title().strip()
            person_up.species = person.species.title().strip()
            person_up.gender = person.gender.title().strip()
            person_up.origin = person.origin.title().strip()
            await session.commit()

            person_up.origin = await get_origin_location(origin = person_up.origin, db = db)
            person_up.location = await get_visit_person(person_id = person_up.id, db = db)
            person_up.url = f'{settings.URI_BASE}/api/v1/person/{person_up.id}'
            return person_up
        else:
            raise HTTPException(detail='Person não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Person
@router.delete('/{person_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_local(person_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Person).filter(Person.id == person_id)
        result = await session.execute(query)
        person_del = result.scalar_one_or_none()

        if person_del:
            await session.delete(person_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Person não encontrado', status_code=status.HTTP_404_NOT_FOUND)
