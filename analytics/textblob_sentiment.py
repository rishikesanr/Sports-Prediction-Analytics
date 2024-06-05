from textblob import TextBlob
import pandas as pd

class TextBlobSentiment:
    def analyze(self, data_fans):
        # Apply TextBlob sentiment analysis
        data_fans['textblob_sentiment'] = data_fans['message'].apply(self.get_sentiment)
        # print("\n\ndata_fans:",data_fans.head(),"\n\n")
        # sentiment_summary = data_fans.groupby('team')['textblob_sentiment'].mean()
        sentiment_summary = data_fans.groupby('team').apply(self.summarize_sentiment)

        return sentiment_summary

    def get_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity


    def summarize_sentiment(self, group):
        total = len(group)
        positive = (group['textblob_sentiment'] > 0).sum()
        negative = (group['textblob_sentiment'] < 0).sum()
        neutral = (group['textblob_sentiment'] == 0).sum()
        
        summary = {
            'negative': negative,
            'neutral': neutral,
            'positive': positive,
            'total': total,
            '%positive': positive / total * 100,
            '%negative': negative / total * 100,
            '%neutral': neutral / total * 100
        }
        return pd.Series(summary)