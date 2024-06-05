import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd

class BertSentiment:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    
    def analyze(self, data_fans):
        # Apply BERT sentiment analysis
        data_fans['bert_sentiment'] = data_fans['message'].apply(self.get_sentiment)
        sentiment_summary = data_fans.groupby('team').apply(self.summarize_sentiment)

        return sentiment_summary

    def get_sentiment(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
        sentiment = predictions.argmax().item()
        return sentiment

    def summarize_sentiment(self, group):
        total = len(group)
        positive = (group['bert_sentiment'] == 4).sum() + (group['bert_sentiment'] == 3).sum()  # 4 and 3 are positive sentiments
        negative = (group['bert_sentiment'] == 0).sum() + (group['bert_sentiment'] == 1).sum()  # 0 and 1 are negative sentiments
        neutral = (group['bert_sentiment'] == 2).sum()  # 2 is neutral sentiment
        
        summary = {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            '%positive': positive / total * 100,
            '%negative': negative / total * 100,
            '%neutral': neutral / total * 100
        }
        return pd.Series(summary)
