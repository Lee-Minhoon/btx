from enum import Enum
from pathlib import Path

RAW_DATA_DIR = Path("data") / "raw"
RESULT_DATA_DIR = Path("data") / "results"


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
