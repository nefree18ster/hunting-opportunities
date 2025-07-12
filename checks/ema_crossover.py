import pandas as pd
import yfinance as yf

def ema_crossover(symbol):
    try:
        # Download 1-hour interval data for the last 3 months
        data = yf.download(symbol, period='3mo', interval='1h')
        if data.empty:
            return f"{symbol}: ❌ No data available"

        # Calculate EMA 5 and EMA 50
        data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

        # Ensure we have enough data to compare
        if len(data) < 2:
            return f"{symbol}: ⚠️ Not enough data"

        # Check for crossover and crossunder
        prev_cross = data['EMA5'].iloc[-2] - data['EMA50'].iloc[-2]
        curr_cross = data['EMA5'].iloc[-1] - data['EMA50'].iloc[-1]

        if prev_cross <= 0 and curr_cross > 0:
            return f"{symbol}: ✅ BUY SIGNAL - 5 EMA crossed above 50 EMA"
        elif prev_cross >= 0 and curr_cross < 0:
            return f"{symbol}: 🔻 SELL SIGNAL - 5 EMA crossed below 50 EMA"
        else:
            return f"{symbol}: ❌ No crossover"

    except Exception as e:
        return f"{symbol}: 🔴 Error - {str(e)}"
