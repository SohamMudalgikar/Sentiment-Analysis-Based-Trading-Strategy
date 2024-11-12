# Get the data 

import yfinance as yf
import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def fetch_stock_data(ticker, period='1y'):
    """
    Fetch historical stock data for the given ticker.
    
    Args:
        ticker (str): Stock ticker symbol.
        period (str): Data period (e.g., '1y', '6mo').
        
    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def fetch_tweets(query, max_tweets=100):
    """
    Fetch recent tweets containing the query.
    
    Args:
        query (str): Search query (e.g., stock ticker).
        max_tweets (int): Maximum number of tweets to fetch.
        
    Returns:
        list: List of tweet texts.
    """
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(max_tweets):
        if 'retweeted_status' in dir(tweet):
            tweets.append(tweet.retweeted_status.full_text)
        else:
            tweets.append(tweet.full_text)
    return tweets
