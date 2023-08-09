from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import desc

from app.Purchases.dao import PurchasesDAO


@pytest.mark.parametrize(
    "id_ticker,vol,purchase_date,selling_date,status_code",
    [
        # *(1,500000, "2023-06-05", "2023-06-19", 200)*4,
        (1, 500000, "2023-06-05", "2023-06-19", 200),
        (1, 500000, "2023-06-05", "2023-06-19", 200),
        (1, 500000, "2023-06-05", "2023-06-19", 200),
        (1, 500000, "2023-06-05", "2023-06-19", 200),
        (1, 500000, "2023-06-05", "2023-06-19", 409),
    ],
)
async def test_add_new_record(
    id_ticker, vol, purchase_date, selling_date, status_code, auth_ac: AsyncClient
):
    r = await auth_ac.post(
        "/holders/new_purchase",
        params={
            "id_ticker": id_ticker,
            "vol": vol,
            "purchase_date": purchase_date,
            "selling_date": selling_date,
        },
    )
    end_purchase = await PurchasesDAO.find_all()

    print(end_purchase[-1].id_tickers)

    # assert end_purchase[-1].id_holders == 1
    assert end_purchase[-1].id_tickers == 1
    assert r.status_code == status_code
