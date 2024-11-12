# Analyze sentiment of a list of tweets. 

from textblob import TextBlob

def analyze_sentiment(tweets):
    """
    Args: tweets (list): List of tweet texts.     
    Returns: float: Average sentiment polarity.
    """
    sentiments = []
    for tweet in tweets:
        blob = TextBlob(tweet)
        sentiments.append(blob.sentiment.polarity)
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    return average_sentiment
