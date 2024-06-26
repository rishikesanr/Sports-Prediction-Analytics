from datetime import datetime
import psycopg2
import pytz
import hashlib

class PostgreSQL:
    def __init__(self, dbname, user, password, host="localhost", port="5432",table="sentiment_analysis_results",
                 league=None,
                 match=None,
                    match_datetime=None,
                    match_result=None,
                    match_scoreline=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table=table
        self.league = league
        self.match=match
        self.match_result = match_result; self.match_scoreline = match_scoreline
        self.match_datetime = datetime.strptime(match_datetime, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        self.run_time = datetime.now(pytz.utc)

        unique_str = f"{self.match}{self.match_datetime}{self.run_time}"
        self.unique_id = hashlib.md5(unique_str.encode()).hexdigest()
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
                (match_run_id,league, match, match_result, scoreline, match_datetime, team, model, total, positive, negative, neutral, percent_positive, percent_negative, 
                            percent_neutral,run_time) 
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                self.unique_id,self.league, self.match, self.match_result, self.match_scoreline, self.match_datetime, team, model_name, total, positive, negative, neutral,
                percent_positive, percent_negative, percent_neutral,self.run_time
            ))

        self.conn.commit()

