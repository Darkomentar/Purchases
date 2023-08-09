from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Holders(Base):
    __tablename__ = "holders"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    purchase = relationship("Purchases", back_populates="holder")

    def __str__(self):
        return f"Holder {self.username}"

    # purchase_prise = Column(Float, nullable=False)
    # volume = Column(Integer, nullable=False)
    # purchase_prise
