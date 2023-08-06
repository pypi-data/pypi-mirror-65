from typing import Optional

from cryptocompsdk.exchanges.info.parse import ExchangesInfo, CouldNotGetExchangeInfoException, exchanges_info_from_dict
from cryptocompsdk.request import APIBase
from cryptocompsdk.urls import EXCHANGE_INFO_URL


class ExchangeInfoAPI(APIBase):
    _exception_class = CouldNotGetExchangeInfoException

    def get(self, to_symbol: Optional[str] = None) -> ExchangesInfo:

        payload = dict(
            tsym=to_symbol,
        )

        return self._get_one_or_paginated(EXCHANGE_INFO_URL, payload)

    def _class_factory(self, data: dict) -> ExchangesInfo:
        return exchanges_info_from_dict(data)
