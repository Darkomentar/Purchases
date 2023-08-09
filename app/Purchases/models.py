from sqlalchemy import Column, Computed, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Purchases(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    id_holders = Column(ForeignKey("holders.id"))
    id_tickers = Column(ForeignKey("tickers.id"))
    purchase_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    purchase_date = Column(Date, nullable=False)
    selling_date = Column(Date, nullable=False)
    delta_day = Column(Integer, Computed("selling_date - purchase_date"))

    holder = relationship("Holders", back_populates="purchase")
    ticker = relationship("Tickers", back_populates="purchase")

    def __str__(self):
        return f"Purchase {self.id}"
