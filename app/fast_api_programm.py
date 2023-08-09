import time
import sys
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI
from os.path import abspath, dirname
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.admin.auth import au_be
from app.admin.views import HoldersAdmin, PurchasesAdmin, TickersAdmin
from app.config import settings
from app.database import engine
from app.Holders.dao import HoldersDAO
from app.Holders.router import router as router_holders
from app.pages.router import router as router_purch
from app.Purchases.router import router as router_purchases
from app.prometeus.router import router as router_prometheus
from app.tasks.tasks import process_mailing
from app.Tickers.router import router as router_tickers
from app.logger import logger


import sentry_sdk


sentry_sdk.init(
    dsn="https://1cb30ec2d882d8d97047dcdb6812964a@o4505671375192064.ingest.sentry.io/4505671387643904",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = FastAPI()
app.include_router(router_tickers)
app.include_router(router_holders)
app.include_router(router_purchases)
app.include_router(router_purch)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_method=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    # allow_method=["*"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Autorization",
    ],
)



app = VersionedFastAPI(app, '{major}', '/v{major}')


instrr = Instrumentator(
    should_group_status_codes= False,
    excluded_handlers=[".*admin.*", "/metrics"]
)

instrr.instrument(app).expose(app)

app.include_router(router_prometheus)

@app.on_event("startup")
def surtup():
    redis = aioredis.from_url(
        settings.BROKER_CELERY, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.get("/mailing")
async def mailing(emtasks: BackgroundTasks, massage: str):
    result = await HoldersDAO.all_mails()
    process_mailing.delay(result, massage)
    # emtasks.add_task(process_mailing, result, massage)
    return "Задание сформировано"
    # return result


admin = Admin(app, engine, authentication_backend=au_be)
admin.add_view(HoldersAdmin)
admin.add_view(PurchasesAdmin)
admin.add_view(TickersAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


# без БД


class STicker(BaseModel):
    name: str
    price: float


tickers = [
    {"name": "SBER", "price": 122.0},
    {"name": "GAZP", "price": 123.0},
    {"name": "NLMK", "price": 124.0},
    {"name": "YNDX", "price": 123.0},
    {"name": "ROSN", "price": 125.0},
    {"name": "VKCO", "price": 126.0},
    {"name": "TNKF", "price": 128.0},
]


class Speople:
    def __init__(self, name: str, age: int, university: str, gender: str):
        self.name = name
        self.age = age
        self.university = university
        self.gender = gender


class SpeopleModel(BaseModel):
    name: str
    age: int
    university: str
    gender: str


@app.get("/tickerss")
@cache(expire=60)
def get_ticers():
    return tickers


@app.get("/tickerss/{tickers_id}")
def get_ticers_by_id(tickers_id: int, name_or_price: bool = None):
    if name_or_price is None:
        return tickers[tickers_id]
    else:
        if name_or_price == False:
            return tickers[tickers_id]["name"]
        else:
            return tickers[tickers_id]["price"]


@app.get("/ticker_search_by_name")
@cache(expire=60)
def ticker_search_by_name(name: str):
    matching_unit = [unit for unit in tickers if unit["name"] == name]
    return matching_unit


@app.get("/tickers_search_by_price")
def tickers_search_by_price(
    low_price: Optional[float] = Query(gt=0, lt=999999),
    high_price: Optional[float] = Query(gt=0, lt=999999),
):
    matching_unit = [
        unit
        for unit in tickers
        if (unit["price"] >= low_price) and (unit["price"] <= high_price)
    ]
    return matching_unit


@app.post("/add_ticker")

def add_ticker(new_ticker: STicker) -> list[STicker]:
    tickers.append({"name": new_ticker.name, "price": new_ticker.price})
    return tickers


@app.get("/return_people")
def return_people(new_people: Speople = Depends()) -> SpeopleModel:
    new_people.age -= -1
    return new_people
