from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Tickers(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    part = Column(Integer, nullable=False)

    purchase = relationship("Purchases", back_populates="ticker")

    def __str__(self):
        return f"ТИКЕР: {self.name}"
