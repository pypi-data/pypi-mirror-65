from typing import Optional

from cryptocompsdk.blockchain.history.parse import CouldNotGetBlockchainHistoryException, BlockchainHistory
from cryptocompsdk.request import APIBase
from cryptocompsdk.urls import BLOCKCHAIN_HISTORICAL_DAILY_URL


class BlockchainHistoryAPI(APIBase):
    _exception_class = CouldNotGetBlockchainHistoryException

    def get(self, from_symbol: str = 'BTC', end_time: Optional[int] = None,
            limit: int = 100, max_api_calls: Optional[int] = None) -> BlockchainHistory:
        payload = dict(
            fsym=from_symbol,
            limit=limit,
            toTs=end_time,
        )

        return self._get_one_or_paginated(BLOCKCHAIN_HISTORICAL_DAILY_URL, payload, max_api_calls=max_api_calls)

    def _class_factory(self, data: dict) -> BlockchainHistory:
        return BlockchainHistory.from_dict(data)
