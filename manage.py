import requests
import pandas as pd
import time
from datetime import datetime, timedelta


API_KEY = "ct6srr1r01qr3sdsr9rgct6srr1r01qr3sdsr9s0"


STOCK_SYMBOLS = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "META", "NFLX", "NVDA", "BRK.A", "JNJ"]


def fetch_realtime_data(symbols, api_key):
    base_url = "https://finnhub.io/api/v1/quote"
    realtime_data = []

    for symbol in symbols:
        params = {"symbol": symbol, "token": api_key}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            realtime_data.append({
                "Symbol": symbol,
                "Current Price": data["c"],
                "High Price": data["h"],
                "Low Price": data["l"],
                "Open Price": data["o"],
                "Previous Close": data["pc"],
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            print(f"Failed to fetch real-time data for {symbol}: {response.text}")
        time.sleep(1)  

   
    realtime_df = pd.DataFrame(realtime_data)
    realtime_df.to_csv("realtime_stock_data.csv", index=False)
    print("Real-time stock data saved to 'realtime_stock_data.csv'.")


def fetch_historical_data(symbols, api_key, months=3):
    base_url = "https://finnhub.io/api/v1/stock/candle"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)

    historical_data = []

    for symbol in symbols:
        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": int(start_date.timestamp()),
            "to": int(end_date.timestamp()),
            "token": api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["s"] == "ok":
                for i in range(len(data["t"])):
                    historical_data.append({
                        "Symbol": symbol,
                        "Date": datetime.fromtimestamp(data["t"][i]).strftime("%Y-%m-%d"),
                        "Open": data["o"][i],
                        "High": data["h"][i],
                        "Low": data["l"][i],
                        "Close": data["c"][i],
                        "Volume": data["v"][i],
                    })
            else:
                print(f"No historical data found for {symbol}.")
        else:
            print(f"Failed to fetch historical data for {symbol}: {response.text}")
        time.sleep(1)  


    historical_df = pd.DataFrame(historical_data)
    historical_df.to_csv("historical_stock_data.csv", index=False)
    print("Historical stock data saved to 'historical_stock_data.csv'.")


def main():
    print("Fetching real-time stock data...")
    fetch_realtime_data(STOCK_SYMBOLS, API_KEY)

    print("Fetching historical stock data...")
    fetch_historical_data(STOCK_SYMBOLS, API_KEY)

if __name__ == "__main__":
    main()
