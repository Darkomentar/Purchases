from datetime import datetime

from sqlalchemy import desc

from app.Purchases.dao import PurchasesDAO


async def test_add_new_record():
    await PurchasesDAO.new_record(
        id_user=1,
        id_ticker=2,
        vol=3904,
        purchase_date=datetime.strptime("2023-06-05", "%Y-%m-%d"),
        selling_date=datetime.strptime("2023-06-19", "%Y-%m-%d"),
    )

    end_purchase = await PurchasesDAO.find_all()

    # print(end_purchase)

    assert end_purchase[-1].id_holders == 1
    assert end_purchase[-1].id_tickers == 2
