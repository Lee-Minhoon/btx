import duckdb
import pandas as pd
import yfinance as yf

from .enum import Interval, Ticker
from .paths import RAW_DATA_DIR, RESULT_DATA_DIR, get_raw_path, get_result_path


def init_dir():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DATA_DIR.mkdir(parents=True, exist_ok=True)


def download(ticker: Ticker, interval: Interval):
    df = yf.download(
        ticker.value,
        start="2000-01-01",
        end="2025-12-31",
        auto_adjust=True,
        interval=interval.value,
    )
    if df is None:
        raise ValueError(f"Failed to download data for {ticker} {interval}")
    df = df.xs(ticker.value, axis=1, level=1)
    path = get_raw_path(ticker, interval)
    df.to_parquet(path, index=True)


def get_raw(ticker: Ticker, interval: Interval):
    return duckdb.read_parquet(str(get_raw_path(ticker, interval)))


def to_csv(ticker: Ticker, interval: Interval):
    df = get_raw(ticker, interval)
    df.to_csv(str(get_result_path(ticker, interval).with_suffix(".csv")))


def save_result(ticker: Ticker, interval: Interval, df: pd.DataFrame):
    df.to_csv(str(get_result_path(ticker, interval)), index=True)


def get_result(ticker: Ticker, interval: Interval):
    return duckdb.read_csv(str(get_result_path(ticker, interval)))
