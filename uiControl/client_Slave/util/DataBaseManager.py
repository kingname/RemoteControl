import pymongo

class DataBaseManager(object):
    def __init__(self, host='127.0.0.1', port=27017):
        connection = pymongo.MongoClient(host, port)
        tdb = connection.webControl
        self.post_info = tdb.test

    def insert(self, info):
        self.post_info.insert(info)

    def find(self, key, value):
        return self.post_info.find({key: value})

    def update(self, _id, key, value):
        self.post_info.update({"_id": _id}, {"$set": {key: value}})
