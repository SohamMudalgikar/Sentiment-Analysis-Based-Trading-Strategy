# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.data_fetcher import fetch_stock_data, fetch_tweets
from utils.sentiment_analysis import analyze_sentiment
from datetime import datetime, timedelta

# Set plotting style
plt.style.use('seaborn')

# Configuration
stock_ticker = 'AAPL'  # Change the ticker to company you want to analyze
tweet_query = 'AAPL'
max_tweets = 100       # Adjust this according to your preference 
data_period = '1y'     

# Fetch stock data
print("Fetching stock data...")
stock_data = fetch_stock_data(stock_ticker, period=data_period)
stock_data.reset_index(inplace=True)

# Fetch tweets
print("Fetching tweets...")
tweets = fetch_tweets(tweet_query, max_tweets=max_tweets)

# Analyze sentiment
print("Analyzing sentiment...")
average_sentiment = analyze_sentiment(tweets)
print(f"Average Sentiment Polarity: {average_sentiment:.2f}")

# Add sentiment to the latest date
latest_date = stock_data['Date'].max()
sentiment_df = pd.DataFrame({
    'Date': [latest_date],
    'Sentiment': [average_sentiment]
})

# Merge sentiment with stock data
stock_data = pd.merge(stock_data, sentiment_df, on='Date', how='left')
stock_data['Sentiment'].fillna(method='ffill', inplace=True)

# Calculate moving averages
stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

# Generate buy/sell signals based on moving averages and sentiment.
def generate_signals(data):
    """
    Args: data (pandas.DataFrame): Stock data with moving averages and sentiment.    
    Returns: pandas.DataFrame: Stock data with signals.
    """
    data['Signal'] = 0
    # Buy signal
    buy_condition = (data['MA50'] > data['MA200']) & (data['Sentiment'] > 0)
    data.loc[buy_condition, 'Signal'] = 1
    # Sell signal
    sell_condition = (data['MA50'] < data['MA200']) & (data['Sentiment'] < 0)
    data.loc[sell_condition, 'Signal'] = -1
    return data

stock_data = generate_signals(stock_data)

# Plotting
plt.figure(figsize=(14,7))
plt.plot(stock_data['Date'], stock_data['Close'], label='Close Price', alpha=0.5)
plt.plot(stock_data['Date'], stock_data['MA50'], label='MA50')
plt.plot(stock_data['Date'], stock_data['MA200'], label='MA200')

# Plot buy signals
buy_signals = stock_data[stock_data['Signal'] == 1]
plt.scatter(buy_signals['Date'], buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)

# Plot sell signals
sell_signals = stock_data[stock_data['Signal'] == -1]
plt.scatter(sell_signals['Date'], sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)

plt.title(f"{stock_ticker} Price with Trading Signals")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.show()

# Display latest sentiment
print(f"Latest Sentiment: {average_sentiment:.2f}")
