"""
Classes and methods for accessing data in database
"""

import os
import re
from typing import List

from pymongo import MongoClient


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

    def read_distinct_movies(self, contains: str) -> List[str]:

        rgx = re.compile(f'.*{contains}.*', re.IGNORECASE)
        movies = self.collection.find({}, {'shows': {'$elemMatch': {'title': rgx}}, '_id': 0})

        all_titles = list()
        for movie in movies:
            shows = movie.get('shows', [])
            shows_titles = [show['title'] for show in shows]
            all_titles.append(shows_titles)

        all_titles_ = list(set(title for shows_titles in all_titles for title in shows_titles))
        return all_titles_

    def read_distinct_cinemas(self) -> List[str]:
        cinemas = self.collection.find({}).distinct('name')
        return cinemas
