from datetime import date
from pprint import pprint

from modules.backtest import Backtest, Trader
from modules.data.enum import Ticker
from modules.utils import get_exchange_rate


def main():
    tickers = list[Ticker](Ticker)
    trader = Trader(100000000 * get_exchange_rate("KRW", "USD"))
    backtest = Backtest(
        trader,
        tickers,
        start_date=date(2000, 1, 1),
        end_date=date(2025, 12, 31),
    )
    result = backtest.run()
    pprint(result)


if __name__ == "__main__":
    main()
