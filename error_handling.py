import logging
from datetime import datetime


logging.basicConfig(filename='portfolio_trades.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')


portfolio = {
    'cash_balance': 10000.00,
    'stocks': {}
}


stock_prices = {
    'AAPL': 150,
    'GOOGL': 2800,
    'AMZN': 3500
}


api_rate_limit = 5
api_calls_made = 0
max_api_calls = api_rate_limit
max_balance = 10000


def get_stock_price(symbol):
    global api_calls_made
    if api_calls_made >= max_api_calls:
        raise Exception("API rate limit exceeded")
    
    if symbol not in stock_prices:
        raise ValueError(f"Missing data for stock: {symbol}")
    
    api_calls_made += 1
    return stock_prices[symbol]


def buy_stock(symbol, quantity):
    global portfolio
    try:
        price = get_stock_price(symbol)
        total_cost = price * quantity

      
        if total_cost > portfolio['cash_balance']:
            raise ValueError(f"Insufficient funds to buy {quantity} of {symbol}.")
        
   
        portfolio['cash_balance'] -= total_cost
        if symbol not in portfolio['stocks']:
            portfolio['stocks'][symbol] = 0
        portfolio['stocks'][symbol] += quantity
        
       
        logging.info(f"BUY - {symbol} - Quantity: {quantity} - Price: {price} - Portfolio Balance: {portfolio['cash_balance']}")
    
    except ValueError as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def sell_stock(symbol, quantity):
    global portfolio
    try:
        if symbol not in portfolio['stocks'] or portfolio['stocks'][symbol] < quantity:
            raise ValueError(f"Not enough shares to sell for {symbol}.")
        
        price = get_stock_price(symbol)
        total_sale = price * quantity
        
        
        portfolio['cash_balance'] += total_sale
        portfolio['stocks'][symbol] -= quantity
        if portfolio['stocks'][symbol] == 0:
            del portfolio['stocks'][symbol]
        

        logging.info(f"SELL - {symbol} - Quantity: {quantity} - Price: {price} - Portfolio Balance: {portfolio['cash_balance']}")
    
    except ValueError as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


try:
    buy_stock('AAPL', 10)
    sell_stock('AAPL', 5)
    buy_stock('GOOGL', 3)
    sell_stock('AMZN', 2)
except Exception as e:
    logging.error(f"Trade simulation error: {e}")


print("Portfolio Status:", portfolio)
