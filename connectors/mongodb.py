from pymongo import MongoClient

class MongoDB:
    def __init__(self, name, collection_name):
        self.name = name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection=None

    def connect(self):
        '''
        Method to create MongoDB database and collection if not exists.
        '''
        # Create a connection to the local mongodb server instance
        self.client = MongoClient("localhost", 27017)
        
        self.db = self.client[self.name]
        self.collection = self.db[self.collection_name]
        
        return self.client, self.db, self.collection