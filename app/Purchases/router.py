from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.Holders.dao import HoldersDAO
from app.Holders.dependencies import get_current_admin, get_current_user
from app.Holders.models import Holders
from app.Purchases.dao import PurchasesDAO

router = APIRouter(prefix="/purchases", tags=["Покупки"])


@router.get("")
@version(1)
async def get_purchases_py_id2(user_data: Holders = Depends(get_current_user)):
    # return user_data
    result = await PurchasesDAO.find_all(id_holders=user_data.id)
    # print(result)
    # print(result)
    return result


@router.get("/all_purchases_admin_function")
@version(1)
@cache(expire=60)
async def get_purchases_py_id(user_data: Holders = Depends(get_current_admin)):
    # return user_data
    return await PurchasesDAO.find_all()
