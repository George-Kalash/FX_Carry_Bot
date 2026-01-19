import pandas as pd

def compute_macd(bars):
    df = pd.DataFrame(bars)
    close = df["close"]

    ema_fast = close.ewm(span=18).mean() # Changed from 12 to 18. Showed a fine result when tested
    ema_slow = close.ewm(span=26).mean()

    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9).mean()
    hist = macd - signal

    return macd.iloc[-1], signal.iloc[-1], hist.iloc[-1]

def compute_ema200(bars):
    df = pd.DataFrame(bars)
    close = df["close"]
    ema200 = close.ewm(span=200).mean()
    return ema200.iloc[-1]



macd_logs = []   # will store previous MACD values



# Trading Logic
 

def should_buy(bars):
    global macd_logs

    if len(bars) < 200:
        return False  # not enough data

    macd, signal, hist = compute_macd(bars)
    ema200 = compute_ema200(bars)
    price = bars[-1]["close"]

    macd_logs.append({
        "macd": macd,
        "signal": signal
    })

    if len(macd_logs) < 2:
        return False

    prev = macd_logs[-2]
    curr = macd_logs[-1]

    # MACD crossover for bullish signal
    bullish_crossover = (
        prev["macd"] < prev["signal"] and
        curr["macd"] > curr["signal"]
    )

    # rossover must happen BELOW zero line to prevent false signals
    below_zero = curr["macd"] < 0 and curr["signal"] < 0

    # Trend filter 
    trend_up = price > ema200

    return bullish_crossover and below_zero and trend_up


def should_sell(bars):
    global macd_logs

    if len(macd_logs) < 2:
        return False

    macd, signal, hist = compute_macd(bars)
    ema200 = compute_ema200(bars)
    price = bars[-1]["close"]

    prev = macd_logs[-2]
    curr = macd_logs[-1]

    # Bearish MACD crossover
    bearish_crossover = (
        prev["macd"] > prev["signal"] and
        curr["macd"] < curr["signal"]
    )

    trend_down = price < ema200
    above_zero = curr["macd"] > 0

    return bearish_crossover and (above_zero or trend_down)
