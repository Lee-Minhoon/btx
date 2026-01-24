from dataclasses import dataclass
from typing import Literal

import pandas as pd
from ta.momentum import StochasticOscillator


def signal_func(row: pd.Series) -> Literal["BUY", "SELL"]:
    return "BUY" if row["stoch_k"] > row["stoch_d"] else "SELL"


@dataclass
class Analyzer:
    df: pd.DataFrame

    def stochastic(self):
        stochastic = StochasticOscillator(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=10,
            smooth_window=3,
        )

        output_df = self.df.copy()
        stoch_k = stochastic.stoch()
        stoch_d = stochastic.stoch_signal()
        stoch_k.index = output_df.index
        stoch_d.index = output_df.index
        output_df["stoch_k"] = stoch_k
        output_df["stoch_d"] = stoch_d
        output_df["signal"] = output_df.apply(signal_func, axis=1)
        return output_df
