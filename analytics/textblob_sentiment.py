from textblob import TextBlob
import pandas as pd

class TextBlobSentiment:
    def analyze(self, data_fans):
        # Apply TextBlob sentiment analysis
        data_fans['textblob_sentiment'] = data_fans['message'].apply(self.get_sentiment)
        print("\n\ndata_fans:",data_fans,"\n\n")
        sentiment_summary = data_fans.groupby('team')['textblob_sentiment'].mean()

        return sentiment_summary

    def get_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

# Example usage:
# textblob_sentiment = TextBlobSentiment()
# sentiment_summary = textblob_sentiment.analyze(data_fans)
# print(sentiment_summary)
