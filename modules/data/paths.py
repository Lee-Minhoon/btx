from .enum import RAW_DATA_DIR, RESULT_DATA_DIR, Interval, Ticker


def get_raw_filename(ticker: Ticker, interval: Interval):
    return f"{ticker.value}_{interval.value}.parquet"


def get_raw_path(ticker: Ticker, interval: Interval):
    return RAW_DATA_DIR / get_raw_filename(ticker, interval)


def get_result_filename(ticker: Ticker, interval: Interval):
    return f"{ticker.value}_{interval.value}.csv"


def get_result_path(ticker: Ticker, interval: Interval):
    return RESULT_DATA_DIR / get_result_filename(ticker, interval)
