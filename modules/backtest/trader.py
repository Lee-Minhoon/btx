from modules.data import Ticker
from modules.utils import annual_roi, roi

from .position import Position


class Trader:
    initial_balance: float
    balance: float
    positions: dict[Ticker, Position]

    def __init__(self, balance: float):
        self.initial_balance = balance
        self.balance = balance
        self.positions = {}

    def _add_position(self, ticker: Ticker):
        self.positions[ticker] = Position(ticker)

    def _remove_position(self, ticker: Ticker):
        self.positions.pop(ticker)

    def buy(self, ticker: Ticker, amount: float, price: float):
        if self.balance < price:
            raise ValueError("Insufficient balance")
        if ticker not in self.positions:
            self._add_position(ticker)
        self.positions[ticker].buy(amount, price)
        self.balance -= price

    def sell(self, ticker: Ticker, amount: float, price: float):
        if ticker not in self.positions:
            return
        if self.positions[ticker].amount < amount:
            raise ValueError("Insufficient balance")
        self.positions[ticker].sell(amount)
        self.balance += price
        if self.positions[ticker].amount == 0:
            self._remove_position(ticker)

    def stock_roi(self, ticker: Ticker):
        return self.positions[ticker].roi()

    def total_roi(self):
        return roi(self.initial_balance, self.balance)

    def annual_roi(self, days: int):
        return annual_roi(self.initial_balance, self.balance, days)

    def buy_count(self):
        return sum(position.buy_count for position in self.positions.values())

    def sell_count(self):
        return sum(position.sell_count for position in self.positions.values())

    def portfolio(self):
        return {
            "balance": self.balance,
            "positions": {
                ticker.value: position.amount
                for ticker, position in self.positions.items()
            },
        }
