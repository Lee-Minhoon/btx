from modules.analyzer import Analyzer
from modules.data import Interval, Ticker, get_raw, init_dir, save_result


def main():
    init_dir()
    for ticker in Ticker:
        # download(ticker, Interval.DAY)
        raw = get_raw(ticker, Interval.DAY).to_df()
        analyzer = Analyzer(raw)
        save_result(ticker, Interval.DAY, analyzer.stochastic())


if __name__ == "__main__":
    main()
