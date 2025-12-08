import pandas as pd
import matplotlib.pyplot as plt

import pattern



def getDf():
    df = pd.read_csv("Data/nvidia_daily.csv")
    droppableColumns = ["Plot", "Plot.1", "Plot.2", "Plot.3"]
    df.drop(droppableColumns, axis=1, inplace=True)
    df = df[(df["time"] >= "2022-01-01") & (df["time"] <= "2024-01-01")]
    detect_patterns(df)
    return df


def showDf(df):
    plt.figure(figsize=(14,6))
    plt.plot(df["time"], df["close"])
    plt.xlabel("Date")
    plt.ylabel("Closing-Price")
    # Als Punktdaten extrahieren
    for pattern_col, color, marker, label in [
        ("bullish_engulfing", "green", "^", "Bullish Engulfing"),
        ("bearish_engulfing", "red", "v", "Bearish Engulfing"),
        ("piercing", "lime", "^", "Piercing Pattern"),
        ("hammer", "darkgreen", "^", "Hammer"),
        ("dark_cloud_cover", "darkred", "v", "Dark Cloud Cover")
    ]:
        idx = df[df[pattern_col] == 1]
        if not idx.empty:
            plt.scatter(idx["time"], idx["close"],
                        color=color, marker=marker, s=80, label=label)

    plt.show()


def detect_patterns(df):
    bullish_engulfing_signals = [0]
    bearish_engulfing_signals = [0]
    piercing_signals = [0]
    hammer_signals = [0]
    dark_cloud_cover_signals = [0]

    for i in range(1, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]

        bullish_engulfing_signals.append(1 if pattern.is_bullish_engulfing(prev, curr) else 0)
        bearish_engulfing_signals.append(1 if pattern.is_bearish_engulfing(prev, curr) else 0)
        piercing_signals.append(1 if pattern.is_piercing(prev, curr) else 0)
        hammer_signals.append(1 if pattern.is_hammer(curr) else 0)  # hammer ist 1-Candle
        dark_cloud_cover_signals.append(1 if pattern.is_dark_cloud_cover(prev, curr) else 0)

    df["bullish_engulfing"] = bullish_engulfing_signals
    df["bearish_engulfing"] = bearish_engulfing_signals
    df["piercing"] = piercing_signals
    df["hammer"] = hammer_signals
    df["dark_cloud_cover"] = dark_cloud_cover_signals

    return df


