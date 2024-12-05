import pandas as pd
import requests
from datetime import datetime


API_KEY = "ct6sda9r01qr3sdspn30ct6sda9r01qr3sdspn3g"


PORTFOLIO = {
    "AAPL": 10,
    "TSLA": 5,
    "AMZN": 7,
    "MSFT": 12,
    "GOOGL": 8
}


def fetch_realtime_data(symbols, api_key):
    base_url = "https://finnhub.io/api/v1/quote"
    current_prices = {}

    for symbol in symbols:
        params = {"symbol": symbol, "token": api_key}
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            current_prices[symbol] = data["c"]  # "c" is the current price
        else:
            print(f"Error fetching data for {symbol}: {response.status_code}")

    return current_prices


def fetch_historical_data(symbols, api_key, months=3):
    base_url = "https://finnhub.io/api/v1/stock/candle"
    historical_prices = {}

    end_date = datetime.now()
    start_date = end_date - pd.DateOffset(months=months)

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
            if data["s"] == "ok" and len(data["c"]) > 0:  
                historical_prices[symbol] = data["c"][0]  
            else:
                print(f"No historical data for {symbol}.")
        else:
            print(f"Error fetching data for {symbol}: {response.status_code}")

    return historical_prices


def calculate_portfolio_value(prices, portfolio):
    total_value = 0
    stock_values = {}

    for symbol, quantity in portfolio.items():
        if symbol in prices:
            stock_value = prices[symbol] * quantity
            stock_values[symbol] = stock_value
            total_value += stock_value

    return total_value, stock_values


def track_performance(current_prices, historical_prices, portfolio):
    performance = []
    total_initial_value = 0
    total_current_value = 0

    for symbol, quantity in portfolio.items():
        if symbol in current_prices and symbol in historical_prices:
            initial_value = historical_prices[symbol] * quantity
            current_value = current_prices[symbol] * quantity
            total_initial_value += initial_value
            total_current_value += current_value

            percentage_change = ((current_value - initial_value) / initial_value) * 100
            performance.append({
                "Symbol": symbol,
                "Initial Value": initial_value,
                "Current Value": current_value,
                "Percentage Change": percentage_change
            })

    overall_percentage_change = ((total_current_value - total_initial_value) / total_initial_value) * 100

    return performance, total_initial_value, total_current_value, overall_percentage_change

# Main Function
def main():
    print("Fetching real-time stock data...")
    current_prices = fetch_realtime_data(PORTFOLIO.keys(), API_KEY)

    print("Fetching historical stock data...")
    historical_prices = fetch_historical_data(PORTFOLIO.keys(), API_KEY)

    print("\nCalculating portfolio value...")
    current_value, stock_values = calculate_portfolio_value(current_prices, PORTFOLIO)
    print(f"Current Portfolio Value: ${current_value:.2f}")

    print("\nTracking portfolio performance...")
    performance, initial_value, current_value, overall_change = track_performance(current_prices, historical_prices, PORTFOLIO)

    
    performance_df = pd.DataFrame(performance)
    print("\nStock Performance:")
    print(performance_df)

    print(f"\nTotal Initial Portfolio Value: ${initial_value:.2f}")
    print(f"Total Current Portfolio Value: ${current_value:.2f}")
    print(f"Overall Portfolio Change: {overall_change:.2f}%")

if __name__ == "__main__":
    main()
