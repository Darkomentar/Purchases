from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.Purchases.models import Purchases
from app.Purchases.router import get_purchases_py_id, get_purchases_py_id2

router = APIRouter(prefix="/pages", tags=["Page"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/purchases")
async def get_purch_pages(
    request: Request, purch_json: Purchases = Depends(get_purchases_py_id2)
):
    print(purch_json)
    return templates.TemplateResponse(
        name="purch.html", context={"request": request, "purch": purch_json}
    )
