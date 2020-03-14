"""
Classes and methods for accessing data in database
"""

import os
import re
from typing import List

from pymongo import MongoClient

from .data_structures import CinemaMovie


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

    def read_distinct_movies(self, contains: str = '') -> List[str]:

        rgx = re.compile(f'.*{contains}.*', re.IGNORECASE)
        cinemas = self.collection.find({},
                                       {'shows': {'$elemMatch': {'title': rgx}},
                                        '_id': 0})

        all_titles = list()
        for cinema in cinemas:
            shows = cinema.get('shows', [])
            shows_titles = [show['title'] for show in shows]
            all_titles.append(shows_titles)

        all_titles_ = list(set(title for shows_titles in all_titles for title in shows_titles))
        return all_titles_

    def read_distinct_cinemas(self, contains: str = '') -> List[str]:

        rgx_name = re.compile(f'.*{contains}.*', re.IGNORECASE)
        cinemas = self.collection.find({'name': rgx_name}).distinct('name')
        return cinemas

    def read_showtimes(self, cinema_name_contains: str = '', movie_title_contains: str = '') \
            -> List[CinemaMovie]:
        """
        Args:
            cinema_name_contains (str):
                substr that should be contained in the cinema name, defaults to ''
            movie_title_contains (str):
                substr that should be contained in the movie title, defaults to ''

        Returns List[CinemaMovie].

        """

        rgx_name = re.compile(f'.*{cinema_name_contains}.*', re.IGNORECASE)
        rgx_title = re.compile(f'.*{movie_title_contains}.*', re.IGNORECASE)
        cinemas = self.collection.find({'name': rgx_name},
                                       {'shows': {'$elemMatch': {'title': rgx_title}},
                                        'name': 1,
                                        '_id': 0})

        cinemamovies = list()
        for cinema in cinemas:
            try:
                [show] = cinema.get('shows', [])
            except ValueError:
                # cinema without shows for this movie
                # or query did not return a single show for cinema cinema['name']
                pass
            else:
                show_times = [t.strftime("%d.%m.%Y, %H:%M:%S") for t in show['times']]

                cinemamovie = CinemaMovie(
                    name=cinema['name'],
                    movie=show['title'],
                    times=show_times
                )

                cinemamovies.append(cinemamovie)
        return cinemamovies
