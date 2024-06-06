from datetime import datetime
import psycopg2
import pytz

class PostgreSQL:
    def __init__(self, dbname, user, password, host="localhost", port="5432",table="sentiment_analysis_results",
                 league=None,
                 match=None,
                    match_datetime=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table=table
        self.league = league
        self.match=match
        self.match_datetime = datetime.strptime(match_datetime, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        self.conn = None
        self.cursor = None

    def connect(self):
        '''
        Method to create a PostgreSQL database connection.
        '''
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def close(self):
        '''
        Method to close the PostgreSQL database connection.
        '''
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_data(self, data, model_name):
        '''
        Method to insert data into the PostgreSQL database.
        '''
        for team, row in data.iterrows():
            # Ensure missing keys are set to 0
            total = row.get('total', 0)
            positive = row.get('positive', 0)
            negative = row.get('negative', 0)
            neutral = row.get('neutral', 0)
            percent_positive = row.get('%positive', 0)
            percent_negative = row.get('%negative', 0)
            percent_neutral = row.get('%neutral', 0)
            
            self.cursor.execute(f"""
                INSERT INTO {self.table} 
                (league, match, match_datetime, team, model, total, positive, negative, neutral, percent_positive, percent_negative, percent_neutral) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                self.league, self.match,self.match_datetime, team, model_name, total, positive, negative, neutral,
                percent_positive, percent_negative, percent_neutral
            ))
        self.conn.commit()

