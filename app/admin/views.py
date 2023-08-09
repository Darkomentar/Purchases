from sqladmin import ModelView

from app.Holders.models import Holders
from app.Purchases.models import Purchases
from app.Tickers.models import Tickers


class HoldersAdmin(ModelView, model=Holders):
    column_list = [Holders.id, Holders.username]
    column_details_exclude_list = [Holders.password]
    can_delete = False
    name = "Холдер"
    name_plural = "Холдеры"
    icon = "fa-solid fa-user"


class PurchasesAdmin(ModelView, model=Purchases):
    column_list = (
        [c.name for c in Purchases.__table__.c] + [Purchases.holder] + [Purchases.ticker]
    )
    name = "Покупка"
    name_plural = "Покупки"
    icon = "fa-solid fa-shopping-cart"


class TickersAdmin(ModelView, model=Tickers):
    column_list = [c.name for c in Tickers.__table__.c]
    name = "Тикер"
    name_plural = "Тикеры"
    icon = "fas fa-chart-line"
