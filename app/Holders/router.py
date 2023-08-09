from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_versioning import version

from app.auth import authenticate_user, create_access_token, get_password_hash
from app.exeptions import NotUserExeption, UserAlreadyExistsException
from app.Holders.dao import HoldersDAO
from app.Holders.dependencies import get_current_user
from app.Holders.models import Holders
from app.Holders.schemas import SHolders, SHoldersAuth
from app.Purchases.dao import PurchasesDAO
from app.Tickers.dao import TickersDAO

router = APIRouter(prefix="/holders", tags=["Холдеры"])


@router.post("/register")
async def register_user1(user_data: SHolders):
    existing_user = await HoldersDAO.find_one_or_none(
        username=user_data.username, email=user_data.email
    )
    if existing_user:
        raise UserAlreadyExistsException()
    hashed_password = get_password_hash(user_data.password)
    await HoldersDAO.add(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        age=user_data.age,
    )


@router.post("/login")
async def register_user2(response: Response, user_data: SHoldersAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise NotUserExeption()
    access_token = create_access_token({"uid": user.id})
    response.set_cookie("holder_access_token", access_token, httponly=True)
    return access_token


@router.get("/logout")
async def register_user3(response: Response):
    response.delete_cookie("holder_access_token")


@router.post("/new_purchase")
@version(1)
async def new_purchase(
    response: Response,
    id_ticker: int,
    vol: int,
    purchase_date: date,
    selling_date: date,
    user_data: Holders = Depends(get_current_user),
):
    await PurchasesDAO.new_record(
        id_user=user_data.id,
        id_ticker=id_ticker,
        vol=vol,
        purchase_date=purchase_date,
        selling_date=selling_date,
    )
    return "Запись успешно занесена"
