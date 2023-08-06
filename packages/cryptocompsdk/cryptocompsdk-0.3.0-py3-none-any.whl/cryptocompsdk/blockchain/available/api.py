from cryptocompsdk.blockchain.available.parse import CouldNotGetBlockchainAvailableCoinsException, \
    BlockchainAvailableCoins
from cryptocompsdk.request import APIBase
from cryptocompsdk.urls import BLOCKCHAIN_AVAILABLE_COINS_URL


class BlockchainAvailableCoinsAPI(APIBase):
    _exception_class = CouldNotGetBlockchainAvailableCoinsException

    def get(self) -> BlockchainAvailableCoins:
        return self._get_one_or_paginated(BLOCKCHAIN_AVAILABLE_COINS_URL)

    def _class_factory(self, data: dict) -> BlockchainAvailableCoins:
        return BlockchainAvailableCoins.from_dict(data)
