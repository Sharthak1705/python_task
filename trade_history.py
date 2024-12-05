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
        "resolution": resolution,  # D = Daily
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
    
    data["Signal"] = None  
    data.loc[data["MA_5"] > data["MA_20"], "Signal"] = "BUY"
    data.loc[data["MA_5"] < data["MA_20"], "Signal"] = "SELL"
    
    return data


def simulate_trades(data, initial_capital=10000):
    """
    Simulate trades based on BUY/SELL signals.
    """
    capital = initial_capital
    portfolio = {}  
    trade_log = []  

    for _, row in data.iterrows():
        if row["Signal"] == "BUY" and capital >= row["close"]:
            # Buy stock
            shares = capital // row["close"]  
            cost = shares * row["close"]
            if shares > 0:
                portfolio[row["date"]] = shares
                capital -= cost
                trade_log.append(f"BUY {shares} shares at {row['close']} on {row['date']}")
        elif row["Signal"] == "SELL" and portfolio:
         
            shares = sum(portfolio.values())
            revenue = shares * row["close"]
            capital += revenue
            portfolio = {}
            trade_log.append(f"SELL {shares} shares at {row['close']} on {row['date']}")

    
    current_portfolio_value = sum(shares * data["close"].iloc[-1] for shares in portfolio.values())
    total_value = capital + current_portfolio_value
    return total_value, capital, current_portfolio_value, trade_log


symbols = ["AAPL", "TSLA", "AMZN", "MSFT"]


for symbol in symbols:
    print(f"\nSimulating trades for {symbol}...")
    try:
        # Fetch historical data
        historical_data = fetch_historical_data(symbol)

        # Generate trade signals
        analyzed_data = moving_average_crossover(historical_data)

        # Simulate trades
        total_value, final_capital, portfolio_value, trade_log = simulate_trades(analyzed_data)

        # Display results
        print(f"Final Capital: ${final_capital:.2f}")
        print(f"Portfolio Value: ${portfolio_value:.2f}")
        print(f"Total Value: ${total_value:.2f}")
        print("\nTrade Log:")
        for log in trade_log:
            print(log)
    except Exception as e:
        print(f"Error simulating trades for {symbol}: {e}")
