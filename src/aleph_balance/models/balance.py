from .base import Base
from sqlalchemy import Column, DateTime, DECIMAL, PrimaryKeyConstraint, String, func


class Balance(Base):
    __tablename__ = "balances"
    __table_args__ = (PrimaryKeyConstraint("address", "currency"),)

    address = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    balance = Column(DECIMAL, nullable=False)
    source = Column(String, nullable=False)
    at_datetime = Column(DateTime, nullable=False, server_default=func.now())
