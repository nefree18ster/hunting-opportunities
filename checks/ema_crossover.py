import pandas as pd
import yfinance as yf

def ema_crossover(symbol):
    try:
        data = yf.download(symbol, period='3mo', interval='1h')
        if data.empty:
            return f"{symbol}: ❌ No data available"

        data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
        data['Crossover'] = data['EMA5'] > data['EMA50']

        if len(data) < 2:
            return f"{symbol}: ⚠️ Not enough data"

        if not data['Crossover'].iloc[-2] and data['Crossover'].iloc[-1]:
            return f"{symbol}: ✅ BUY SIGNAL - 5 EMA crossed above 50 EMA"
        return f"{symbol}: ❌ No crossover"

    except Exception as e:
        return f"{symbol}: 🔴 Error - {str(e)}"
