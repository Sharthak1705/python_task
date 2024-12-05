import pandas as pd
import requests


API_KEY = "ct6srr1r01qr3sdsr9rgct6srr1r01qr3sdsr9s0"


def fetch_historical_data(symbol, resolution="D", days=60):
    """
    Fetch historical data for a stock from Finnhub API.
    """
    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,  
        "count": days,
        "token": API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200 and data.get("s") == "ok":
        return pd.DataFrame({
            "date": pd.to_datetime(data["t"], unit="s"),
            "close": data["c"]
        })
    else:
        raise Exception(f"Failed to fetch data for {symbol}. Response: {data}")


def moving_average_crossover(data, short_window=5, long_window=20):
    """
    Calculate moving averages and generate BUY/SELL signals.
    """
    data["MA_5"] = data["close"].rolling(window=short_window).mean()
    data["MA_20"] = data["close"].rolling(window=long_window).mean()
    
    data["Signal"] = "HOLD"  # Default signal
    data.loc[data["MA_5"] > data["MA_20"], "Signal"] = "BUY"
    data.loc[data["MA_5"] < data["MA_20"], "Signal"] = "SELL"
    
    return data


symbols = ["AAPL", "TSLA", "AMZN", "MSFT"]


for symbol in symbols:
    print(f"\nAnalyzing {symbol}...")
    try:
       
        historical_data = fetch_historical_data(symbol)
  

        analyzed_data = moving_average_crossover(historical_data)
        
        
        trade_signals = analyzed_data[analyzed_data["Signal"] != "HOLD"]
        print(trade_signals[["date", "Signal", "close"]])
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
