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



macd_logs = []   # this is required to store previous MACD values


STOP_LOSS_BUFFER = 0.995  # 0.5% below EMA200

def should_buy(bars):
    """
    Returns True if buy conditions are met:
    - MACD crosses above signal below zero line
    - Price above EMA200
    """
    global macd_logs
    if len(bars) < 200:
        return False, None  # Not enough data

    price = bars[-1]["close"]
    ema200 = compute_ema200(bars)
    macd, signal, hist = compute_macd(bars)

    # this will add current MACD to logs
    macd_logs.append({"macd": macd, "signal": signal, "price": price})

    if len(macd_logs) < 2:
        return False, None

    prev = macd_logs[-2]
    curr = macd_logs[-1]

    # MACD crossover
    bullish_crossover = prev["macd"] < prev["signal"] and curr["macd"] > curr["signal"]
    below_zero = curr["macd"] < 0 and curr["signal"] < 0
    trend_up = price > ema200

    if bullish_crossover and below_zero and trend_up:
        stop_loss = ema200 * STOP_LOSS_BUFFER
        return True, stop_loss
    return False, None

def should_sell(bars, entry_price=None):
    """
    Returns True if sell conditions are met:
    - MACD crosses below signal above zero line
    - Price below EMA200
    - Or price hits stop-loss
    """
    global macd_logs
    if len(macd_logs) < 2:
        return False

    price = bars[-1]["close"]
    ema200 = compute_ema200(bars)
    macd, signal, hist = compute_macd(bars)

    prev = macd_logs[-2]
    curr = macd_logs[-1]

    # Bearish crossover
    bearish_crossover = prev["macd"] > prev["signal"] and curr["macd"] < curr["signal"]
    above_zero = curr["macd"] > 0
    trend_down = price < ema200

    stop_loss_hit = entry_price is not None and price < ema200 * STOP_LOSS_BUFFER

    if bearish_crossover and (above_zero or trend_down):
        return True
    if stop_loss_hit:
        return True

    return False


