import pymongo

class Database(object):
    URI="mongodb://localhost:27017/"
    DATABASE=None

    @staticmethod
    def initialize():
        client=pymongo.MongoClient(Database.URI)
        Database.DATABASE=client['Recommendation_system']

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_one_id(collection,query, queryy):
        return Database.DATABASE[collection].find_one(query,queryy)

    @staticmethod
    def update_one(collection, query, queryy):
        Database.DATABASE[collection].update(query,queryy)