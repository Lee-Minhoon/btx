import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator
from ta.trend import ADXIndicator


class StochasticOscillatorAnalyzer:
    df: pd.DataFrame
    stochastic: StochasticOscillator

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.stochastic = StochasticOscillator(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        )
        self.df["stoch_k"] = self.stochastic.stoch()
        self.df["stoch_d"] = self.stochastic.stoch_signal()
        self.df["signal"] = "HOLD"

    def oversold(self) -> pd.Series:
        return self.df["stoch_k"] < 20

    def overbought(self) -> pd.Series:
        return self.df["stoch_k"] > 80

    def cross_up(self) -> pd.Series:
        prev_k = self.df["stoch_k"].shift(1)
        prev_d = self.df["stoch_d"].shift(1)
        return (prev_k <= prev_d) & (self.df["stoch_k"] > self.df["stoch_d"])

    def cross_down(self) -> pd.Series:
        prev_k = self.df["stoch_k"].shift(1)
        prev_d = self.df["stoch_d"].shift(1)
        return (prev_k >= prev_d) & (self.df["stoch_k"] < self.df["stoch_d"])

    def adx(self) -> pd.Series:
        return ADXIndicator(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
        ).adx()

    # 모멘텀 거리 가중치 (0 ~ 1)
    def distance_weight(self) -> pd.Series:
        distance = (self.df["stoch_k"] - self.df["stoch_d"]).abs() / 100
        return distance.clip(0, 1)

    # 구간 가중치 (0 ~ 1)
    def zone_weight(self) -> pd.Series:
        zone_weight = np.where(
            self.df["signal"] == "BUY",
            (20 - self.df["stoch_k"]) / 20,
            np.where(
                self.df["signal"] == "SELL",
                (self.df["stoch_k"] - 80) / 20,
                0,
            ),
        )
        return pd.Series(zone_weight, index=self.df.index).clip(0, 1)

    # 기울기 가중치 (0 ~ 1)
    def slope_weight(self) -> pd.Series:
        prev_k = self.df["stoch_k"].shift(1)
        slope_weight = (self.df["stoch_k"] - prev_k).abs() / 10
        return slope_weight.clip(0, 1)

    # 추세 강도 가중치 (0 ~ 1)
    def trend_weight(self) -> pd.Series:
        trend_weight = self.adx() / 30
        return trend_weight.clip(0, 1)

    def analyze(self) -> pd.DataFrame:
        trend_weight = self.trend_weight()

        # 강한 추세장일 때는 신호를 무시
        self.df.loc[
            self.cross_up() & self.oversold() & (trend_weight < 0.7),
            "signal",
        ] = "BUY"

        # 강한 추세장일 때는 신호를 무시
        self.df.loc[
            self.cross_down() & self.overbought() & (trend_weight < 0.7),
            "signal",
        ] = "SELL"

        # 4️⃣ 최종 강도 조합
        raw_strength = (
            0.4 * self.distance_weight()
            + 0.3 * self.zone_weight()
            + 0.2 * self.slope_weight()
            + 0.1 * (1 - trend_weight)
        )

        self.df["strength"] = raw_strength.clip(0, 1)

        return self.df[["stoch_k", "stoch_d", "signal", "strength"]]
