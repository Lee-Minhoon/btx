from dataclasses import dataclass
from datetime import date
from typing import TypedDict

import pandas as pd

from modules.data import Ticker
from modules.utils import get_exchange_rate

from .trader import Trader


class BacktestConfig(TypedDict):
    trader: Trader
    df: pd.DataFrame
    start_date: date
    end_date: date


class BacktestReport(TypedDict):
    balance: float
    initial_balance: float
    total_value: float
    roi: float
    years: float
    annual_roi: float
    buy_count: int
    sell_count: int


@dataclass
class Backtest:
    trader: Trader
    df: pd.DataFrame
    start_date: date
    end_date: date

    def run(self):
        df = self.df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        actual_start = max(df.index.min().date(), self.start_date)
        actual_end = min(df.index.max().date(), self.end_date)
        df = df.loc[actual_start:actual_end]

        for _, row in df.iterrows():
            self.trader.update(Ticker.MICROSOFT, row["Close"])
            if row["signal"] == "BUY":
                self.trader.buy(Ticker.MICROSOFT, 1, row["Close"])
            elif row["signal"] == "SELL":
                self.trader.sell(Ticker.MICROSOFT, 1, row["Close"])

        rate = get_exchange_rate("USD", "KRW")

        return BacktestReport(
            balance=self.trader.balance * rate,
            initial_balance=self.trader.initial_balance * rate,
            total_value=self.trader.total_value() * rate,
            roi=self.trader.total_roi(),
            years=(actual_end - actual_start).days / 365,
            annual_roi=self.trader.annual_roi((actual_end - actual_start).days),
            buy_count=self.trader.buy_count(),
            sell_count=self.trader.sell_count(),
        )
