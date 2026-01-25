from dataclasses import dataclass
from datetime import date
from typing import TypedDict

import pandas as pd

from modules.data import Interval, Ticker, get_result
from modules.utils import get_exchange_rate

from .position import PositionReport
from .trader import Trader


class BacktestReport(TypedDict):
    initial_balance: float
    balance: float
    total_value: float
    roi: float
    years: float
    annual_roi: float
    buy_count: int
    sell_count: int
    per_ticker: dict[Ticker, PositionReport]


@dataclass
class Backtest:
    trader: Trader
    tickers: list[Ticker]
    start_date: date
    end_date: date

    def run(self):
        dataframes: dict[Ticker, pd.DataFrame] = {}
        for ticker in self.tickers:
            df = get_result(ticker, Interval.DAY).to_df()
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
            df = df.loc[self.start_date : self.end_date]
            dataframes[ticker] = df
            self.trader.add_position(ticker)

        start_date = min(df.index.min().date() for df in dataframes.values())
        end_date = max(df.index.max().date() for df in dataframes.values())

        for current_date in pd.date_range(start_date, end_date):
            for ticker, df in dataframes.items():
                if current_date not in df.index:
                    continue
                row = df.loc[current_date].to_dict()
                self.trader.update(ticker, row["Close"])
                if row["signal"] == "BUY":
                    self.trader.buy(ticker, 1, row["Close"])
                elif row["signal"] == "SELL":
                    self.trader.sell(ticker, 1, row["Close"])

        rate = get_exchange_rate("USD", "KRW")
        days = (end_date - start_date).days

        return BacktestReport(
            initial_balance=self.trader.initial_balance * rate,
            balance=self.trader.balance * rate,
            total_value=self.trader.total_value() * rate,
            roi=self.trader.total_roi(),
            years=days / 365,
            annual_roi=self.trader.annual_roi(days),
            buy_count=self.trader.buy_count(),
            sell_count=self.trader.sell_count(),
            per_ticker={
                ticker: self.trader.positions[ticker].report()
                for ticker in self.tickers
            },
        )
