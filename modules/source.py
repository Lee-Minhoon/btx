import duckdb
from pathlib import Path
import yfinance as yf
from enum import Enum

DATA_DIR = Path("data")


class Interval(Enum):
    DAY = "1d"
    WEEK = "1wk"
    MONTH = "1mo"


class Ticker(Enum):
    MICROSOFT = "MSFT"
    APPLE = "AAPL"
    ALPHABET = "GOOGL"
    AMAZON = "AMZN"
    COCA_COLA = "KO"
    DISNEY = "DIS"
    FACEBOOK = "FB"
    GOOGLE = "GOOGL"
    IBM = "IBM"


class Extension(Enum):
    PARQUET = "parquet"
    CSV = "csv"


def getName(ticker: Ticker, interval: Interval):
    return f"{ticker.value}_{interval.value}.parquet"


def getPath(ticker: Ticker, interval: Interval):
    return DATA_DIR / getName(ticker, interval)


def download(
    ticker: Ticker, interval: Interval, extension: Extension = Extension.PARQUET
):
    df = yf.download(
        ticker.value,
        start="2000-01-01",
        end="2025-12-31",
        auto_adjust=True,
        interval=interval.value,
    )
    if df is None:
        raise ValueError(f"Failed to download data for {ticker} {interval}")
    match extension:
        case Extension.PARQUET:
            df.to_parquet(getPath(ticker, interval))
        case Extension.CSV:
            df.to_csv(getPath(ticker, interval).with_suffix(".csv"))


def read(ticker: Ticker, interval: Interval):
    return duckdb.read_parquet(str(getPath(ticker, interval)))


def toCsv(ticker: Ticker, interval: Interval):
    df = read(ticker, interval)
    df.to_csv(str(getPath(ticker, interval).with_suffix(".csv")))


def main():
    download(Ticker.MICROSOFT, Interval.DAY, Extension.CSV)
    download(Ticker.MICROSOFT, Interval.DAY, Extension.PARQUET)


if __name__ == "__main__":
    main()
