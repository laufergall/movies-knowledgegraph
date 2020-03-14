""""
Includes the endpoints for namespace movies
"""

from flask_restplus import Namespace, Resource
from .db_access import MongoDBConnector


db_accessor = MongoDBConnector()

api = Namespace('movies',
                description='Retrieve information about movies.')


@api.route('/titles')
class Movies(Resource):

    def get(self):
        """
        Retrieve movie titles in Berlin cinemas
        """

        titles = db_accessor.read_distinct_movies()
        return titles
