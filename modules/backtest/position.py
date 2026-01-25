from typing import TypedDict

from modules.data import Ticker
from modules.utils import roi


class PositionReport(TypedDict):
    value: float
    roi: float
    total_cost: float
    buy_count: int
    sell_count: int


class Position:
    ticker: Ticker
    amount: float
    current_price: float
    avg_buy_price: float
    buy_count: int
    sell_count: int
    realized_profit: float
    unrealized_profit: float

    def __init__(self, ticker: Ticker):
        self.ticker = ticker
        self.realized_profit = 0
        self.buy_count = 0
        self.sell_count = 0
        self.initialize()

    def initialize(self):
        self.amount = 0
        self.current_price = 0
        self.avg_buy_price = 0
        self.unrealized_profit = 0

    def buy(self, amount: float, price: float):
        if amount < 0 or price < 0:
            raise ValueError("Amount or price is negative")
        cost = price * amount
        total_cost = self.total_cost() + cost
        self.amount += amount
        self.avg_buy_price = total_cost / self.amount
        self.buy_count += 1

    def sell(self, amount: float):
        if amount < 0:
            raise ValueError("Amount is negative")
        if self.amount < amount:
            raise ValueError("Insufficient amount")
        self.amount -= amount
        self.sell_count += 1
        realized_profit = (self.current_price - self.avg_buy_price) * amount
        self.realized_profit += realized_profit
        if self.amount == 0:
            self.initialize()
        return realized_profit

    def update(self, price: float):
        self.current_price = price
        self.unrealized_profit = (price - self.avg_buy_price) * self.amount

    def total_cost(self):
        return self.avg_buy_price * self.amount

    def value(self):
        return self.current_price * self.amount

    def roi(self):
        return roi(self.total_cost(), self.value())

    def report(self):
        return PositionReport(
            value=self.value(),
            total_cost=self.total_cost(),
            roi=self.roi(),
            buy_count=self.buy_count,
            sell_count=self.sell_count,
        )
