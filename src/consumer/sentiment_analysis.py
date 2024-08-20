# src/consumer/sentiment_analysis.py
from textblob import TextBlob

class SentimentAnalyzer:
    def analyze(self, tags):
        blob = TextBlob(tags)
        return blob.sentiment.polarity  # Return sentiment polarity (-1 to 1)
