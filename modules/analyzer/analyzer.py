from dataclasses import dataclass

import pandas as pd
from ta.momentum import RSIIndicator

from modules.analyzer.stochastic import StochasticOscillatorAnalyzer


@dataclass
class Analyzer:
    df: pd.DataFrame

    def stochastic(self):
        analyzer = StochasticOscillatorAnalyzer(self.df)
        return self.df.join(analyzer.analyze())

    def rsi(self):
        rsi = RSIIndicator(
            close=self.df["Close"],
        )
        output_df = self.df.copy()
        rsi = rsi.rsi()
        rsi.index = output_df.index
        output_df["rsi"] = rsi
        return output_df
