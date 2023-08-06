from copy import deepcopy
from dataclasses import dataclass
from typing import Any, List, Optional

import pandas as pd

from cryptocompsdk.general.parse import (
    from_int,
    from_none,
    from_union,
    from_float,
    from_str,
    to_float,
    from_bool,
    from_list,
    to_class,
)
from cryptocompsdk.response import ResponseAPIBase, ResponseException


@dataclass
class BlockchainHistoryRecord:
    id: Optional[int] = None
    symbol: Optional[str] = None
    time: Optional[int] = None
    zero_balance_addresses_all_time: Optional[int] = None
    unique_addresses_all_time: Optional[int] = None
    new_addresses: Optional[int] = None
    active_addresses: Optional[int] = None
    transaction_count: Optional[int] = None
    transaction_count_all_time: Optional[int] = None
    large_transaction_count: Optional[int] = None
    average_transaction_value: Optional[float] = None
    block_height: Optional[float] = None
    hashrate: Optional[float] = None
    difficulty: Optional[float] = None
    block_time: Optional[float] = None
    block_size: Optional[float] = None
    current_supply: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> "BlockchainHistoryRecord":
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        symbol = from_union([from_str, from_none], obj.get("symbol"))
        time = from_union([from_int, from_none], obj.get("time"))
        zero_balance_addresses_all_time = from_union(
            [from_int, from_none], obj.get("zero_balance_addresses_all_time")
        )
        unique_addresses_all_time = from_union(
            [from_int, from_none], obj.get("unique_addresses_all_time")
        )
        new_addresses = from_union([from_int, from_none], obj.get("new_addresses"))
        active_addresses = from_union(
            [from_int, from_none], obj.get("active_addresses")
        )
        transaction_count = from_union(
            [from_int, from_none], obj.get("transaction_count")
        )
        transaction_count_all_time = from_union(
            [from_int, from_none], obj.get("transaction_count_all_time")
        )
        large_transaction_count = from_union(
            [from_int, from_none], obj.get("large_transaction_count")
        )
        average_transaction_value = from_union(
            [from_float, from_none], obj.get("average_transaction_value")
        )
        block_height = from_union([from_float, from_none], obj.get("block_height"))
        hashrate = from_union([from_float, from_none], obj.get("hashrate"))
        difficulty = from_union([from_float, from_none], obj.get("difficulty"))
        block_time = from_union([from_float, from_none], obj.get("block_time"))
        block_size = from_union([from_float, from_none], obj.get("block_size"))
        current_supply = from_union([from_float, from_none], obj.get("current_supply"))
        return BlockchainHistoryRecord(
            id,
            symbol,
            time,
            zero_balance_addresses_all_time,
            unique_addresses_all_time,
            new_addresses,
            active_addresses,
            transaction_count,
            transaction_count_all_time,
            large_transaction_count,
            average_transaction_value,
            block_height,
            hashrate,
            difficulty,
            block_time,
            block_size,
            current_supply,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["symbol"] = from_union([from_str, from_none], self.symbol)
        result["time"] = from_union([from_int, from_none], self.time)
        result["zero_balance_addresses_all_time"] = from_union(
            [from_int, from_none], self.zero_balance_addresses_all_time
        )
        result["unique_addresses_all_time"] = from_union(
            [from_int, from_none], self.unique_addresses_all_time
        )
        result["new_addresses"] = from_union([from_int, from_none], self.new_addresses)
        result["active_addresses"] = from_union(
            [from_int, from_none], self.active_addresses
        )
        result["transaction_count"] = from_union(
            [from_int, from_none], self.transaction_count
        )
        result["transaction_count_all_time"] = from_union(
            [from_int, from_none], self.transaction_count_all_time
        )
        result["large_transaction_count"] = from_union(
            [from_int, from_none], self.large_transaction_count
        )
        result["average_transaction_value"] = from_union(
            [to_float, from_none], self.average_transaction_value
        )
        result["block_height"] = from_union([from_float, from_none], self.block_height)
        result["hashrate"] = from_union([from_float, from_none], self.hashrate)
        result["difficulty"] = from_union([from_float, from_none], self.difficulty)
        result["block_time"] = from_union([to_float, from_none], self.block_time)
        result["block_size"] = from_union([from_float, from_none], self.block_size)
        result["current_supply"] = from_union(
            [from_float, from_none], self.current_supply
        )
        return result

    @property
    def is_empty(self) -> bool:
        is_empty_cols = [
            'zero_balance_addresses_all_time',
            'unique_addresses_all_time',
            'new_addresses',
            'active_addresses',
            'transaction_count',
            'transaction_count_all_time',
            'large_transaction_count',
            'average_transaction_value',
            'block_height',
            'hashrate',
            'difficulty',
            'block_time',
            'block_size',
            'current_supply',
        ]
        for col in is_empty_cols:
            if getattr(self, col) != 0:
                return False
        return True


@dataclass
class Data:
    data: List[BlockchainHistoryRecord]
    aggregated: Optional[bool] = None
    time_from: Optional[int] = None
    time_to: Optional[int] = None

    def __post_init__(self):
        if self.data is None:
            self.data = []

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        aggregated = from_union([from_bool, from_none], obj.get("Aggregated"))
        time_from = from_union([from_int, from_none], obj.get("TimeFrom"))
        time_to = from_union([from_int, from_none], obj.get("TimeTo"))
        data = from_union(
            [lambda x: from_list(BlockchainHistoryRecord.from_dict, x), from_none], obj.get("Data")
        )
        return Data(data, aggregated, time_from, time_to)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Aggregated"] = from_union([from_bool, from_none], self.aggregated)
        result["TimeFrom"] = from_union([from_int, from_none], self.time_from)
        result["TimeTo"] = from_union([from_int, from_none], self.time_to)
        result["Data"] = from_union(
            [lambda x: from_list(lambda x: to_class(BlockchainHistoryRecord, x), x), from_none], self.data
        )
        return result

    def __add__(self, other):
        out_obj = deepcopy(self)
        out_obj.data += other.data
        out_obj.time_from = min(out_obj.time_from, other.time_from)
        out_obj.time_to = max(out_obj.time_to, other.time_to)
        return out_obj

    def __radd__(self, other):
        out_obj = deepcopy(other)
        out_obj.data += self.data
        out_obj.time_from = min(out_obj.time_from, self.time_from)
        out_obj.time_to = max(out_obj.time_to, self.time_to)
        return out_obj


@dataclass
class RateLimit:
    pass

    @staticmethod
    def from_dict(obj: Any) -> "RateLimit":
        assert isinstance(obj, dict)
        return RateLimit()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class BlockchainHistory(ResponseAPIBase):
    data: Data
    response: Optional[str] = None
    message: Optional[str] = None
    has_warning: Optional[bool] = None
    type: Optional[int] = None
    rate_limit: Optional[RateLimit] = None

    def __post_init__(self):
        if self.data is None:
            self.data = []

    @staticmethod
    def from_dict(obj: Any) -> "BlockchainHistory":
        assert isinstance(obj, dict)
        response = from_union([from_str, from_none], obj.get("Response"))
        message = from_union([from_str, from_none], obj.get("Message"))
        has_warning = from_union([from_bool, from_none], obj.get("HasWarning"))
        type = from_union([from_int, from_none], obj.get("Type"))
        rate_limit = from_union([RateLimit.from_dict, from_none], obj.get("RateLimit"))
        data = from_union([Data.from_dict, from_none], obj.get("Data"))
        return BlockchainHistory(data, response, message, has_warning, type, rate_limit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Response"] = from_union([from_str, from_none], self.response)
        result["Message"] = from_union([from_str, from_none], self.message)
        result["HasWarning"] = from_union([from_bool, from_none], self.has_warning)
        result["Type"] = from_union([from_int, from_none], self.type)
        result["RateLimit"] = from_union(
            [lambda x: to_class(RateLimit, x), from_none], self.rate_limit
        )
        result["Data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        return result

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.to_dict()['Data']['Data'])
        if 'time' in df.columns:
            df['time'] = df['time'].apply(pd.Timestamp.fromtimestamp)
        return df

    # Pagination methods

    # TODO [#9]: think about restructuring pagination parse methods
    #
    # There is a lot of repeated code for pagination between blockchain history and price history
    # in the parse classes. If any additional history APIs are added and they follow the same
    # format, this should certainly be restructured into base classes.

    @property
    def is_empty(self) -> bool:
        for record in self.data.data:
            if not record.is_empty:
                return False

        return True

    def __add__(self, other):
        out_obj = deepcopy(self)
        out_obj.data += other.data
        return out_obj

    def __radd__(self, other):
        out_obj = deepcopy(other)
        out_obj.data += self.data
        return out_obj

    @property
    def time_from(self) -> int:
        if self.data.time_from is None:
            raise ValueError('could not determine time from as it is not in the data')
        return self.data.time_from

    def delete_record_matching_time(self, time: int):
        times = [record.time for record in self.data.data]
        try:
            idx = times.index(time)
        except ValueError:
            raise CouldNotGetBlockchainHistoryException(f'tried removing overlapping time {time} but was not in data')
        del self.data.data[idx]

    def trim_empty_records_at_beginning(self):
        self.data.data.reverse()  # now earliest records are at end

        # Delete, starting from end, oldest record
        for i, record in reversed(list(enumerate(self.data.data))):
            if record.is_empty:
                del self.data.data[i]
            else:
                # First non-empty record from end, we have now hit the actual data section, stop deleting
                break

        self.data.data.reverse()  # restore original order, earliest records at beginning


class CouldNotGetBlockchainHistoryException(ResponseException):
    pass
