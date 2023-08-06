import typing
import datetime

from shioaji.base import BaseModel
from shioaji.constant import TickType, ChangeType, Exchange


class Ticks(BaseModel):
    ts: typing.List[int]
    close: typing.List[float]
    volume: typing.List[int]
    bid_price: typing.List[float]
    bid_volume: typing.List[int]
    ask_price: typing.List[float]
    ask_volume: typing.List[int]

    def lazy_setter(self, **kwargs):
        [
            setattr(self, kwarg, value)
            for kwarg, value in kwargs.items()
            if hasattr(self, kwarg)
        ]


class Snapshot(BaseModel):
    ts: int
    code: str
    exchange: str
    open: float
    high: float
    low: float
    close: float
    tick_type: TickType
    change_price: float
    change_rate: float
    change_type: ChangeType
    average_price: float
    volume: int
    total_volume: int
    amount: int
    total_amount: int
    yesterday_volume: float
    buy_price: float
    buy_volume: float
    sell_price: float
    sell_volume: int
    volume_ratio: float


class Snapshots(BaseModel):
    snapshot: typing.List[Snapshot]

