import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from scipy.signal import find_peaks

def detect_latest_reverse_divergence(symbol):
    try:
        df = yf.download(symbol, period='6mo', interval='1d', auto_adjust=True)
        if df.empty or len(df) < 30:
            return f"{symbol}: 🔴 Error - Not enough data"

        df = df[['Close']].dropna()  # Make sure 'Close' is the only column and no NaNs

        close_series = df['Close'].squeeze()  # Ensure it's a Series
        rsi_series = RSIIndicator(close_series).rsi()

        close_prices = close_series.to_numpy()
        rsi_values = rsi_series.to_numpy()

        # Detect peaks in price and RSI
        price_peaks, _ = find_peaks(close_prices)
        rsi_peaks, _ = find_peaks(rsi_values)

        # Detect troughs (inverse peaks)
        price_troughs, _ = find_peaks(-close_prices)
        rsi_troughs, _ = find_peaks(-rsi_values)

        # Look for bullish reverse divergence
        if len(price_troughs) >= 2 and len(rsi_troughs) >= 2:
            p1, p2 = price_troughs[-2], price_troughs[-1]
            r1, r2 = rsi_troughs[-2], rsi_troughs[-1]
            if close_prices[p2] < close_prices[p1] and rsi_values[r2] > rsi_values[r1]:
                date = df.index[p2].strftime('%Y-%m-%d')
                return f"{symbol} - ✅ Bullish reverse divergence on {date}"

        # Look for bearish reverse divergence
        if len(price_peaks) >= 2 and len(rsi_peaks) >= 2:
            p1, p2 = price_peaks[-2], price_peaks[-1]
            r1, r2 = rsi_peaks[-2], rsi_peaks[-1]
            if close_prices[p2] > close_prices[p1] and rsi_values[r2] < rsi_values[r1]:
                date = df.index[p2].strftime('%Y-%m-%d')
                return f"{symbol} - ❌ Bearish reverse divergence on {date}"

        return ""  # No divergence found

    except Exception as e:
        return f"{symbol}: 🔴 Error - {e}"
