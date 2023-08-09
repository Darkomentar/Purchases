import asyncio

# import datetime
import json
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, engine, gen_session
from app.fast_api_programm import app
from app.Holders.models import Holders
from app.Purchases.models import Purchases
from app.Tickers.models import Tickers


# @pytest.mark.asyncio
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    holders = open_mock_json("holders")
    tickers = open_mock_json("tickers")
    purchases = open_mock_json("purchases")

    for purchase in purchases:
        purchase["purchase_date"] = datetime.strptime(
            purchase["purchase_date"], "%Y-%m-%d"
        )
        purchase["selling_date"] = datetime.strptime(purchase["selling_date"], "%Y-%m-%d")

    async with gen_session() as session:
        add_holders = insert(Holders).values(holders)
        add_tickers = insert(Tickers).values(tickers)
        add_purchases = insert(Purchases).values(purchases)

        await session.execute(add_holders)
        await session.execute(add_tickers)
        await session.execute(add_purchases)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/holders/login", json={"email": "tech@ninja.com", "password": "string"}
        )
        assert ac.cookies["holder_access_token"]
        yield ac
