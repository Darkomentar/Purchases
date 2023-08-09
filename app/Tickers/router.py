from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.database import gen_session
from app.Tickers.dao import TickersDAO
from app.Tickers.models import Tickers
from app.Tickers.schemas import STickers

router = APIRouter(prefix="/tickers", tags=["Тикеры"])


@router.get("")
async def get_tickers() -> list[STickers]:
    result = await TickersDAO.find_all()
    return result


@router.get("/exept_test")
async def exept_testt():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test ERROR"
    )


# @router.get("")
# async def get_tickers():
#     async with gen_session() as session:
#         query = select(Ticers)
#         result  = await session.execute(query)
#         return result.scalars().all()

# @router.get("/test")
# async def get_tickers():
#     async with gen_session() as session:
#         query = select(Ticers)
#         result  = await session.execute(query)
#         return result.mappings().all()


# @router.get("/{tickers_id}")
# def get_tickers_by_id(tickers_id):
#     pass
