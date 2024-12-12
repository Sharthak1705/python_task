# Stock Portfolio Tracker and Trade Analyzer

## Overview
This project is a **Stock Portfolio Tracker and Trade Analyzer** designed to manage and analyze stock portfolios using real-world data. The application provides insights, generates trade signals, and simulates trades based on historical and real-time stock data.

---

## Features

### Part 1: Data Collection
- **Fetch Real-Time Data**: Uses a public stock API (e.g., Alpha Vantage, Yahoo Finance) to fetch real-time stock prices for 10 symbols (e.g., AAPL, TSLA, AMZN, MSFT).
- **Historical Data**: Downloads historical data for the past 3 months and stores it separately in a local file (CSV).

### Part 2: Portfolio Tracker
- **Simulated Portfolio**: Tracks a user's stock holdings and calculates the current value using real-time data.
- **Performance Tracking**: Compares the portfolio's value over time and calculates percentage gains or losses for each stock.

### Part 3: Trade Analyzer
- **Trade Signal Generation**:
  - Implements a Moving Average Crossover Strategy.
  - Generates BUY/SELL signals based on the 5-day and 20-day moving averages.
- **Trade History Simulation**:
  - Simulates trades with an initial capital of $10,000.
  - Outputs final capital and portfolio value after 3 months.

### Part 4: Error Handling and Logging
- Handles errors such as API rate limits and missing data.
- Logs trades with details such as date, stock symbol, action (BUY/SELL), quantity, price, and portfolio balance.

### Bonus Features
- **Data Visualization**: Plots stock prices over time and highlights BUY/SELL signals.
- **Custom Strategy**: Allows user-defined thresholds for moving averages to test performance.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `pandas` for data manipulation.
  - `matplotlib` and `seaborn` for visualization.
  - `requests` for API calls.
  - `sqlite3` for local data storage.
  - `logging` for error handling and trade logging.

---

## How to Run the Project

### Prerequisites
1. Install Python 3.9 or later.
2. Install the required libraries:
   ```bash
   pip install pandas matplotlib seaborn requests
   ```

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Sharthak1705/python_task
   cd stock-portfolio-tracker
   ```
2. Set up your API key:
   - Create an account on a stock API provider (e.g.,Finnhub).
   - Add your API key to the `.env` file:
     ```env
     API_KEY=your_api_key_here
     ```
3. Run the program:
   ```bash
   python main.py
   ```

## Future Enhancements
- Integrate more advanced trading strategies.
- Add support for more stock APIs.
- Develop a web-based interface using Flask or Django.

---

## License
This project is open-source and available under the MIT License.
