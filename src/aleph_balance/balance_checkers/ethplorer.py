import logging
from typing import Dict, List
from decimal import Decimal

import aiohttp

from aleph_balance.models.balance import Balance
from .balance_checker import ALEPH_CONTRACT_ID, BalanceChecker

LOGGER = logging.getLogger("balance.ethplorer")

API_URL_TEMPLATE = "https://api.ethplorer.io/getAddressInfo/{address}?apiKey={api_key}"


class EthplorerBalanceChecker(BalanceChecker):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch_token_data(self, address: str):
        api_url = API_URL_TEMPLATE.format(address=address, api_key=self.api_key)

        # TODO: Check if using the freekey api key is acceptable
        async with aiohttp.ClientSession() as client:
            async with client.get(api_url) as resp:
                resp.raise_for_status()
                return await resp.json()

    @staticmethod
    def parse_balance(token: Dict) -> Decimal:
        balance = Decimal(token["rawBalance"])
        decimals = token["tokenInfo"]["decimals"]
        decimals = Decimal(decimals)
        # Check value consistency:
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        if decimals != int(decimals):
            raise ValueError("Decimals must be an integer")
        if decimals < 1:
            raise ValueError("Decimals must be greater than 1")
        return balance / 10 ** decimals

    async def get_balances(self, address: str) -> List[Balance]:
        result = await self.fetch_token_data(address)

        if "error" in result:
            raise ValueError(f"Ethplorer error: {result['error']['message']} ({result['error']['code']}).")

        return [
            Balance(
                address=address,
                currency=token["tokenInfo"]["symbol"],
                balance=self.parse_balance(token),
                source="api.ethplorer.io",

            )
            for token in result.get("tokens", ())
        ]
