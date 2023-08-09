from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exeptions import (
    FieldExpirationExeption,
    FieldTokenExeption,
    NotAdminExeption,
    NotUIDExeption,
    NotUIDinDBExeption,
)
from app.Holders.dao import HoldersDAO
from app.Holders.models import Holders


def get_token(request: Request):
    token = request.cookies.get("holder_access_token")
    if not token:
        raise FieldTokenExeption()
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        jwt_decode = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise FieldTokenExeption()
    expire: str = jwt_decode.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise FieldExpirationExeption()
    user_id: str = jwt_decode.get("uid")
    if not user_id:
        raise NotUIDExeption()
    user = await HoldersDAO.find_by_id(user_id)
    if not user:
        raise NotUIDinDBExeption()

    return user


async def get_current_admin(cuser: Holders = Depends(get_current_user)):
    # if cuser.role != "admin":
    #     raise NotAdminExeption()
    # return cuser
    # -----------------ТУТ ДОЛЖНА БЫТЬ ПРОВЕРКА НА АДМИНА
    pass
    return cuser
