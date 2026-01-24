from datetime import date

from modules.backtest import Backtest, Trader
from modules.data import Interval, Ticker, get_result


def main():
    result = get_result(Ticker.MICROSOFT, Interval.DAY).to_df()
    trader = Trader(1000000)
    backtest = Backtest(
        trader, result, start_date=date(2000, 1, 1), end_date=date(2025, 12, 31)
    )
    result = backtest.run()
    print(result)


if __name__ == "__main__":
    main()
