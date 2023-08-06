from dataclasses import dataclass
from typing import Optional, Dict, List

import pandas as pd

from cryptocompsdk.general.parse import from_int, from_none, from_union, from_str, from_bool, \
    from_dict, to_class
from cryptocompsdk.response import ResponseAPIBase, ResponseException


@dataclass
class AvailableCoin:
    id: Optional[int] = None
    symbol: Optional[str] = None
    partner_symbol: Optional[str] = None
    data_available_from: Optional[int] = None

    @staticmethod
    def from_dict(obj: dict) -> 'AvailableCoin':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        symbol = from_union([from_str, from_none], obj.get("symbol"))
        partner_symbol = from_union([from_str, from_none], obj.get("partner_symbol"))
        data_available_from = from_union([from_int, from_none], obj.get("data_available_from"))
        return AvailableCoin(id, symbol, partner_symbol, data_available_from)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["symbol"] = from_union([from_str, from_none], self.symbol)
        result["partner_symbol"] = from_union([from_str, from_none], self.partner_symbol)
        result["data_available_from"] = from_union([from_int, from_none], self.data_available_from)
        return result


@dataclass
class RateLimit:
    pass

    @staticmethod
    def from_dict(obj: dict) -> 'RateLimit':
        assert isinstance(obj, dict)
        return RateLimit()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class BlockchainAvailableCoins(ResponseAPIBase):
    data: Dict[str, AvailableCoin]
    response: Optional[str] = None
    message: Optional[str] = None
    has_warning: Optional[bool] = None
    type: Optional[int] = None
    rate_limit: Optional[RateLimit] = None


    @staticmethod
    def from_dict(obj: dict) -> 'BlockchainAvailableCoins':
        assert isinstance(obj, dict)
        response = from_union([from_str, from_none], obj.get("Response"))
        message = from_union([from_str, from_none], obj.get("Message"))
        has_warning = from_union([from_bool, from_none], obj.get("HasWarning"))
        type = from_union([from_int, from_none], obj.get("Type"))
        rate_limit = from_union([RateLimit.from_dict, from_none], obj.get("RateLimit"))
        data = from_union([lambda x: from_dict(AvailableCoin.from_dict, x), from_none], obj.get("Data"))
        return BlockchainAvailableCoins(data, response, message, has_warning, type, rate_limit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Response"] = from_union([from_str, from_none], self.response)
        result["Message"] = from_union([from_str, from_none], self.message)
        result["HasWarning"] = from_union([from_bool, from_none], self.has_warning)
        result["Type"] = from_union([from_int, from_none], self.type)
        result["RateLimit"] = from_union([lambda x: to_class(RateLimit, x), from_none], self.rate_limit)
        result["Data"] = from_union([lambda x: from_dict(lambda x: to_class(AvailableCoin, x), x), from_none], self.data)
        return result

    @property
    def symbol_list(self) -> List[str]:
        return [symbol for symbol in self.data]

    @property
    def symbol_id_dict(self) -> Dict[str, int]:
        return {symbol: coin.id for symbol, coin in self.data.items() if symbol is not None and coin.id is not None}

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame([ac.to_dict() for ac in self.data.values()])
        if 'data_available_from' in df.columns:
            df['data_available_from'] = df['data_available_from'].apply(pd.Timestamp.fromtimestamp)
        return df


class CouldNotGetBlockchainAvailableCoinsException(ResponseException):
    pass
