from pydantic import BaseModel
from decimal import Decimal


class BalanceSchema(BaseModel):
    class Config:
        orm_mode = True

    address: str
    currency: str
    balance: Decimal
