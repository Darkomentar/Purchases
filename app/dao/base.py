from sqlalchemy import *
from sqlalchemy.orm import *

# sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from app.database import gen_session

# import sys
# from os.path import abspath, dirname



class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with gen_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with gen_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with gen_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with gen_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


# BaseDAO.find_all()
