from dataclasses import dataclass

import pandas as pd
from ta.momentum import RSIIndicator

from modules.analyzer.stochastic import compute_stochastic


@dataclass
class Analyzer:
    df: pd.DataFrame

    def stochastic(self):
        return self.df.join(compute_stochastic(self.df))

    def rsi(self):
        rsi = RSIIndicator(
            close=self.df["Close"],
        )
        output_df = self.df.copy()
        rsi = rsi.rsi()
        rsi.index = output_df.index
        output_df["rsi"] = rsi
        return output_df
