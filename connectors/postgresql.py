import psycopg2

class PostgreSQL:
    def __init__(self, dbname, user, password, host="localhost", port="5432",table="sentiment_analysis_results"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.table=table
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
            self.cursor.execute(f"""
                INSERT INTO {self.table} 
                (team, model, total, positive, negative, neutral, percent_positive, percent_negative, percent_neutral) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                team, model_name, row['total'], row['positive'], row['negative'], row['neutral'],
                row['%positive'], row['%negative'], row['%neutral']
            ))
        self.conn.commit()
œ