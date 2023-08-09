from pydantic import BaseModel


class STickers(BaseModel):
    id: int
    name: str
    price: int
    volume: int
    part: int
