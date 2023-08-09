from datetime import date, datetime

from fastapi import Depends
from sqlalchemy import Insert, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import gen_session
from app.exeptions import CustomExeptions, NotVolExeption
from app.Holders.models import Holders
from app.Purchases.models import Purchases
from app.Tickers.dao import TickersDAO
from app.Tickers.models import Tickers
from app.logger import logger


class PurchasesDAO(BaseDAO):
    model = Purchases

    @classmethod
    async def check_volume(cls, id_ticker: int, vol: int):
        ticker = await TickersDAO.find_by_id(id_ticker)
        if ticker.volume < vol:
            raise NotVolExeption()
        return ticker

    @classmethod
    async def new_record(
        cls,
        id_user: int,
        id_ticker: int,
        vol: int,
        purchase_date: date,
        selling_date: date,
    ):
        # try:
            ticker = await PurchasesDAO.check_volume(id_ticker, vol)
            async with gen_session() as session:
                query = insert(Purchases).values(
                    {
                        "id_holders": id_user,
                        "id_tickers": id_ticker,
                        "purchase_price": ticker.price,
                        "volume": vol,
                        "purchase_date": purchase_date,
                        "selling_date": selling_date,
                    }
                )
                await session.execute(query)
                await session.commit()
            async with gen_session() as session:
                stmt = (
                    update(Tickers)
                    .where(Tickers.id == id_ticker)
                    .values(volume=(ticker.volume - vol))
                )
                await session.execute(stmt)
                await session.commit()
        # except (SQLAlchemyError, Exception, CustomExeptions, NotVolExeption) as e:
        #     msg = "Unknown Exc"
        #     if isinstance(e, SQLAlchemyError):
        #         msg = "Database Exc"
        #     msg += ": Cannot add purchase"
        #     extra =  {
        #         "id_user" : id_user,
        #         "id_ticker" : id_ticker,
        #         "vol" : vol,
        #         "purchase_date" : purchase_date,
        #         "selling_date" : selling_date,
        #     }
        #     logger.error(msg, extra=extra, exc_info=True)

