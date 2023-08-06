from typing import Dict, Optional

from cryptocompsdk.blockchain.available.api import BlockchainAvailableCoinsAPI
from cryptocompsdk.blockchain.history.api import BlockchainHistoryAPI
from cryptocompsdk.coins.parse import Coins
from cryptocompsdk.exchanges.info.api import ExchangeInfoAPI
from cryptocompsdk.exchanges.symbols.api import ExchangeSymbolsAPI
from cryptocompsdk.request import APIBase
from cryptocompsdk.history.api import HistoryAPI
from cryptocompsdk.coins.api import CoinsAPI
from cryptocompsdk.social.current.api import SocialLatestAPI
from cryptocompsdk.social.history.api import SocialHistoryAPI


class CryptoCompare(APIBase):
    """
    The main interface to the API. Contains objects which represent individual API endpoints.

    history :class:`.HistoryAPI`

    coins :class:`.CoinsAPI`

    social_history :class:`.SocialHistoryAPI`

    social_latest :class:`.SocialLatestAPI`

    exchange_symbols :class:`.ExchangeSymbolsAPI`

    exchange_info :class:`.ExchangeInfoAPI`

    blockchain_available_coins :class:`.BlockchainAvailableCoinsAPI`

    blockchain_history :class:`.BlockchainHistoryAPI`
    """

    def __init__(self, api_key: str, throttle: Optional[float] = None):
        super().__init__(api_key, throttle)
        self.history = HistoryAPI(api_key, throttle)
        self.coins = CoinsAPI(api_key, throttle)
        self.social_history = SocialHistoryAPI(api_key, throttle)
        self.social_latest = SocialLatestAPI(api_key, throttle)
        self.exchange_symbols = ExchangeSymbolsAPI(api_key, throttle)
        self.exchange_info = ExchangeInfoAPI(api_key, throttle)
        self.blockchain_available_coins = BlockchainAvailableCoinsAPI(api_key, throttle)
        self.blockchain_history = BlockchainHistoryAPI(api_key, throttle)

        self._coin_response: Optional[Coins] = None

    @property
    def coin_ids(self) -> Dict[str, int]:
        try:
            return self._coin_response.symbol_id_dict  # type: ignore
        except AttributeError:
            self._coin_response = self.coins.get()
            return self._coin_response.symbol_id_dict
