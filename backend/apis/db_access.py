"""
Classes and methods for accessing data in database
"""

from pymongo import MongoClient
import os
from typing import List


class MongoDBConnector:

    def __init__(self):

        client = MongoClient(
            host=os.environ.get('MONGODB_HOST'),
            port=int(os.environ.get('MONGODB_PORT')),
            username=os.environ.get('MONGODB_USERNAME'),
            password=os.environ.get('MONGODB_PASSWORD'),
        )
        db = client[os.environ.get('MONGODB_DB')]
        self.collection = db[os.environ.get('MONGODB_COLLECTION')]

    def read_distinct_movies(self) -> List[str]:
        movies = self.collection.find({}).distinct('shows.title')
        return movies

    def read_distinct_cinemas(self) -> List[str]:
        cinemas = self.collection.find({}).distinct('name')
        return cinemas
