import abc
from typing import List

from aleph_balance.models.balance import Balance

ALEPH_CONTRACT_ID = "0x27702a26126e0b3702af63ee09ac4d1a084ef628"


class BalanceChecker(abc.ABC):
    @abc.abstractmethod
    async def get_balances(self, address: str) -> List[Balance]:
        ...
