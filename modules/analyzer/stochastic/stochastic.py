import numpy as np
import pandas as pd
from ta.momentum import StochasticOscillator
from ta.trend import ADXIndicator


def compute_stochastic(df: pd.DataFrame) -> pd.DataFrame:
    stochastic = StochasticOscillator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
    )
    result = pd.DataFrame(index=df.index)

    result["stoch_k"] = stochastic.stoch()
    result["stoch_d"] = stochastic.stoch_signal()

    prev_k = result["stoch_k"].shift(1)
    prev_d = result["stoch_d"].shift(1)

    result["signal"] = "HOLD"

    result.loc[
        (prev_k <= prev_d)
        & (result["stoch_k"] > result["stoch_d"])
        & (result["stoch_k"] < 20),
        "signal",
    ] = "BUY"

    result.loc[
        (prev_k >= prev_d)
        & (result["stoch_k"] < result["stoch_d"])
        & (result["stoch_k"] > 80),
        "signal",
    ] = "SELL"

    # ADX (추세 강도)
    adx = ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
    ).adx()

    # (1) K-D 거리
    distance_weight = (result["stoch_k"] - result["stoch_d"]).abs() / 100
    distance_weight = distance_weight.clip(0, 1)

    # (2) 구간 가중치
    zone_weight = np.where(
        result["signal"] == "BUY",
        (20 - result["stoch_k"]) / 20,
        np.where(
            result["signal"] == "SELL",
            (result["stoch_k"] - 80) / 20,
            0,
        ),
    )
    zone_weight = pd.Series(zone_weight, index=df.index).clip(0, 1)

    # (3) 기울기
    slope_weight = (result["stoch_k"] - prev_k).abs() / 10
    slope_weight = slope_weight.clip(0, 1)

    # (4) 추세 강도 (ADX)
    trend_weight = (adx / 30).clip(0, 1)

    # 4️⃣ 최종 강도 조합
    raw_strength = (
        0.4 * distance_weight
        + 0.3 * zone_weight
        + 0.2 * slope_weight
        + 0.1 * trend_weight
    )

    result["strength"] = raw_strength.clip(0, 1)

    return result[["stoch_k", "stoch_d", "signal", "strength"]]
