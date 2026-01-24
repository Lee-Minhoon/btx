from modules.data import Ticker
from modules.utils import roi


class Position:
    ticker: Ticker
    invested: float
    amount: float
    current_price: float
    avg_price: float
    buy_count: int
    sell_count: int
    unrealized_profit: float

    def __init__(self, ticker: Ticker):
        self.ticker = ticker
        self.invested = 0
        self.amount = 0
        self.current_price = 0
        self.avg_price = 0
        self.buy_count = 0
        self.sell_count = 0
        self.unrealized_profit = 0

    def buy(self, amount: float, price: float):
        if amount < 0 or price < 0:
            raise ValueError("Amount or price is negative")
        cost = price * amount
        value = self.value() + cost
        self.invested += cost
        self.amount += amount
        self.avg_price = value / self.amount
        self.buy_count += 1

    def sell(self, amount: float):
        if amount < 0:
            raise ValueError("Amount is negative")
        if self.amount < amount:
            raise ValueError("Insufficient amount")
        self.invested -= self.avg_price * amount
        self.amount -= amount
        self.sell_count += 1

        realized_profit = (self.current_price - self.avg_price) * amount
        return realized_profit

    def update(self, price: float):
        self.current_price = price
        self.unrealized_profit = (price - self.avg_price) * self.amount

    def value(self):
        return self.avg_price * self.amount

    def roi(self):
        return roi(self.invested, self.value())
