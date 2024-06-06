import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class BagOfWords:
    def __init__(self):
        self.vectorizer = CountVectorizer()

    def analyze(self, data_fans):
        X = self.vectorizer.fit_transform(data_fans['message'])
        word_freq = pd.DataFrame(X.toarray(), columns=self.vectorizer.get_feature_names_out()).sum()
        top_30_words = word_freq.nlargest(30)
        
        sentiment_words = {'disrespectful': 1, 'cant': -1, 'last': -1, 'least': -1, 'like': 1, 'strength': 1, 'win': 1, 'lose': -1}
        vectorizer_sentiment_scores = CountVectorizer(vocabulary=sentiment_words.keys())
        X_sentiment_scores = vectorizer_sentiment_scores.fit_transform(data_fans['message'])
        
        df_sentiment_scores = pd.DataFrame(X_sentiment_scores.toarray(), columns=vectorizer_sentiment_scores.get_feature_names_out())
        
        for word, score in sentiment_words.items():
            df_sentiment_scores[word] *= score

        # print("\n\mData:",data_fans,"\n\n")
              
        data_fans = pd.concat([data_fans, df_sentiment_scores], axis=1)
        data_fans['sentiment_score'] = data_fans.iloc[:, 2:].sum(axis=1)
        # Apply sentiment labels
        data_fans['sentiment_label'] = data_fans['sentiment_score'].apply(
            lambda x: "positive" if x > 0 else ("negative" if x < 0 else "neutral")
        )

        # Group by team and sentiment label, count occurrences
        sentiment_props = data_fans.groupby('team')['sentiment_label'].value_counts().unstack().fillna(0)

        # Calculate total counts
        sentiment_props['total'] = sentiment_props.sum(axis=1)

        # Calculate percentage columns, using .get() to provide a default value of 0 if the column is missing
        sentiment_props['%positive'] = sentiment_props.get('positive', 0) / sentiment_props['total'] * 100
        sentiment_props['%negative'] = sentiment_props.get('negative', 0) / sentiment_props['total'] * 100
        sentiment_props['%neutral'] = sentiment_props.get('neutral', 0) / sentiment_props['total'] * 100

        # Optional: Ensure all percentage columns are present
        sentiment_props['%positive'] = sentiment_props['%positive'].fillna(0)
        sentiment_props['%negative'] = sentiment_props['%negative'].fillna(0)
        sentiment_props['%neutral'] = sentiment_props['%neutral'].fillna(0)

        # print(sentiment_props)
        # sentiment_props['win_percentage'] = (sentiment_props['positive'] /sentiment_props['total'] )* 100
        
        # total_win_percentage = sentiment_props['positive'].sum() / sentiment_props['total'].sum() * 100
        # sentiment_props['normalized_win_percentage'] = sentiment_props['win_percentage'] / total_win_percentage * 100
        
        return sentiment_props

