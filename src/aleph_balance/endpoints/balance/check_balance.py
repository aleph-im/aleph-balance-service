from .router import router
from aleph_balance.schemas.balance_schemas import BalanceSchema
from aleph_balance.models.balance import Balance
from fastapi import Depends
from sqlalchemy import select
from typing import List
from aleph_balance.db import get_db_session
from aleph_balance.balance_checkers.ethplorer import EthplorerBalanceChecker


balance_checker = EthplorerBalanceChecker(api_key="freekey")


@router.get("/{address}", response_model=List[BalanceSchema])
async def get_balance(address: str, session=Depends(get_db_session)):
    balances = await balance_checker.get_balances(address)
    session.add_all(balances)
    return balances
