import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


data = {
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07'],
    'AAPL': [150, 152, 154, 153, 155, 157, 159],
    'GOOGL': [2800, 2825, 2850, 2875, 2900, 2925, 2950],
    'AMZN': [3500, 3520, 3535, 3550, 3575, 3600, 3620]
}


df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])


def calculate_signals(df, short_window, long_window):
    signals = pd.DataFrame(index=df.index)
    for symbol in df.columns[1:]:  # Iterate over stock symbols (ignoring 'Date' column)
        signals[symbol] = pd.Series(index=df.index)
        short_rolling = df[symbol].rolling(window=short_window).mean()
        long_rolling = df[symbol].rolling(window=long_window).mean()

        signals[symbol + '_short'] = short_rolling
        signals[symbol + '_long'] = long_rolling
        
        signals[symbol + '_signal'] = np.where(short_rolling > long_rolling, 1, 0)
        signals[symbol + '_position'] = signals[symbol + '_signal'].diff()
        
    return signals

def custom_strategy(df, short_window=3, long_window=5):
    signals = calculate_signals(df, short_window, long_window)
    
    
    plt.figure(figsize=(10, 6))
    
    for symbol in df.columns[1:]:
        plt.plot(df['Date'], df[symbol], label=f'{symbol} Price', linewidth=1.5)
        plt.plot(df['Date'], signals[symbol + '_short'], label=f'{symbol} Short MA ({short_window})', linestyle='--')
        plt.plot(df['Date'], signals[symbol + '_long'], label=f'{symbol} Long MA ({long_window})', linestyle=':')
        
        
        buy_signals = df['Date'][signals[symbol + '_position'] == 1]
        sell_signals = df['Date'][signals[symbol + '_position'] == -1]
        
        plt.scatter(buy_signals, df[symbol][signals[symbol + '_position'] == 1], marker='^', color='g', label='Buy Signal', alpha=1)
        plt.scatter(sell_signals, df[symbol][signals[symbol + '_position'] == -1], marker='v', color='r', label='Sell Signal', alpha=1)

    plt.title(f"Stock Prices and Moving Averages for Custom Strategy")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.show()


short_window = 3  
long_window = 5   

custom_strategy(df, short_window, long_window)
