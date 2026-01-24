from modules.source import Interval, Ticker, read
from modules.analyzer import Analyzer


def main():
    df = read(Ticker.MICROSOFT, Interval.DAY)
    analyzer = Analyzer(df)
    print(analyzer.describe())


if __name__ == "__main__":
    main()
