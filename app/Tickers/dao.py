from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import gen_session
from app.Tickers.models import Tickers


class TickersDAO(BaseDAO):
    model = Tickers
    # @classmethod
    # async def find_all(cls):
    #     async with gen_session() as session:
    #         query = select(Ticers)
    #         result  = await session.execute(query)
    #         return result.scalars().all()
