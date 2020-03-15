"""
Classes and methods for accessing data in database
"""

import json
import os
import re
from typing import List, Union

from pymongo import MongoClient

from .data_structures import Cinema, CinemaMovie


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
        """ Returns distinct movie titles where name like *contains*. """

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
        """ Returns distinct cinema names where name like *contains*. """

        rgx_name = re.compile(f'.*{contains}.*', re.IGNORECASE)
        cinemas = self.collection.find({'name': rgx_name}).distinct('name')
        return cinemas

    def read_cinema_details(self, name: str) -> Union[Cinema, None]:
        """ Returns all fields except for shows for cinema where name = name . """

        cinema = self.collection.find_one({'name': name}, {'_id': 0, 'shows': 0})
        if cinema is None:
            return None
        return Cinema.from_json(json.dumps(cinema))

    def read_cinema_shows(self, name: str) -> List[dict]:
        """ Returns all show titles and times for cinema where name = name . """

        cinema = self.collection.find_one({'name': name}, {'shows': 1})

        shows_ = list()
        for show in cinema.get('shows', []):
            times = sorted([t for t in show['times']])
            show.update(
                {'times': [t.strftime('%A, %d.%m.%Y, %H:%M') for t in times]})
            shows_.append(show)
        return shows_

    def read_showtimes(self, cinema_name_contains: str = '', movie_title_contains: str = '') \
            -> List[CinemaMovie]:
        """
        Returns cinema name, first matching movie title, and its show times
        where cinema name like *contains*.

        Args:
            cinema_name_contains (str):
                substr that should be contained in the cinema name, defaults to ''
            movie_title_contains (str):
                substr that should be contained in the movie title, defaults to ''

        Returns List[CinemaMovie].

        None:
            For each cinema, the first movie matching the given string is returned.
            Only cinemas for which a movie is found are returned.
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
                show_times = sorted([t for t in show['times']])
                show_times_ = [t.strftime('%A, %d.%m.%Y, %H:%M') for t in show_times]

                cinemamovie = CinemaMovie(
                    name=cinema['name'],
                    movie=show['title'],
                    times=show_times_
                )

                cinemamovies.append(cinemamovie)
        return cinemamovies
