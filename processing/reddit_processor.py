import pandas as pd
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime, timedelta
from nltk.stem import WordNetLemmatizer
from connectors.mongodb import MongoDB
import string

# Load the necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re

class RedditProcessor:
    def __init__(self, db_name, collection_name,match_date_time):
        self.db_name = db_name
        self.match_date = re.findall(r'(\d{4}-\d{2}-\d{2})',match_date_time)[0]
        self.collection_name = f"{collection_name.lower().replace(' ','-')}-{self.match_date}"
        # self.collection_name = "arsenal-vs-everton-2024-05-19" # for testing
        self.mongo = MongoDB(self.db_name, self.collection_name)
        self.client, self.db, self.collection = self.mongo.connect()

    def transform_label_reddit_data(self, match, doc_list):
        keywords = [team.lower() for team in match.split(' vs ')]
        rows = []

        for doc in doc_list:
            title = doc.get('title', '')
            description = doc.get('description', '')
            comments = doc.get('comments', [])

            messages = [title, description] + comments

            for message in messages:
                message = message.lower()

                if keywords[0] in message and keywords[1] not in message:
                    rows.append({"team": keywords[0], "message": message})
                elif keywords[1] in message and keywords[0] not in message:
                    rows.append({"team": keywords[1], "message": message})

        return pd.DataFrame(rows)

    def preprocess_text(self, text):
        lemmatizer = WordNetLemmatizer()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
        return ' '.join(words)

    def process_data(self, match):
        doc_list = [doc for doc in self.client[self.db_name][self.collection_name].find({"source": "reddit"})]
        data_fans = self.transform_label_reddit_data(match, doc_list)
        data_fans['message'] = data_fans['message'].apply(self.preprocess_text)
        return data_fans
