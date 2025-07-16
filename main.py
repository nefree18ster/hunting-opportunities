from checks.ema_crossover import ema_crossover
from checks.reverse_divergence import detect_latest_reverse_divergence
from utils import read_stock_list, log_result
from notifier import send_telegram_alert  # 🚨 Telegram notifier

# def run_ema_check():
#     stock_list = read_stock_list("stocks.txt")
#     for symbol in stock_list:
#         result = ema_crossover(symbol)
#         # Filter for only buy or sell signals
#         if "BUY SIGNAL" in result or "SELL SIGNAL" in result:
#             print(result)
#             log_result(result, "logs/ema_crossover.log")
#             send_telegram_alert(result)

def run_reverse_divergence_check():
    stock_list = read_stock_list("stocks.txt")
    for symbol in stock_list:
        result = detect_latest_reverse_divergence(symbol)
        print(f"{symbol}: {result}")
        if "Bullish" in result or "Bearish" in result:
            print(result)
            log_result(result, "logs/reverse_divergence.log")

if __name__ == "__main__":
    # run_ema_check()
    run_reverse_divergence_check()

