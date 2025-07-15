# checks/ema_crossover.py

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def ema_crossover(symbol):
    try:
        # Download hourly data for last 5 days
        data = yf.download(symbol, period='5d', interval='1h', progress=False)
        if data.empty:
            return f"{symbol}: ❌ No data available"

        # Compute EMAs
        data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

        # Normalize date
        data['Date'] = data.index.tz_localize(None).date

        # Identify yesterday
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        # Filter for only yesterday’s candles
        yesterday_data = data[data['Date'] == yesterday]
        if yesterday_data.empty:
            return f"{symbol}: ⚠️ No data for yesterday ({yesterday})"

        # Check for crossover / crossunder in yesterday
        for i in range(1, len(yesterday_data)):
            prev = yesterday_data.iloc[i - 1]
            curr = yesterday_data.iloc[i]

            prev_diff = prev['EMA5'] - prev['EMA50']
            curr_diff = curr['EMA5'] - curr['EMA50']

            if prev_diff <= 0 and curr_diff > 0:
                return f"{symbol}: ✅ BUY SIGNAL - 5 EMA crossed above 50 EMA"
            elif prev_diff >= 0 and curr_diff < 0:
                return f"{symbol}: 🔻 SELL SIGNAL - 5 EMA crossed below 50 EMA"

        return f"{symbol}: ❌ No crossover or crossunder yesterday"

    except Exception as e:
        return f"{symbol}: 🔴 Error - {str(e)}"
