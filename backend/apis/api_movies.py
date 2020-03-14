""""
Includes the endpoints for namespace movies
"""

from flask_restplus import Namespace, Resource, reqparse

from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

title_parser = reqparse.RequestParser()
title_parser.add_argument(name='contains',
                          default='',
                          required=False,
                          help='substr to be contained in the movie title')

api = Namespace('movies',
                description='Retrieve information about movies.')


@api.route('/titles')
class Movies(Resource):

    @api.expect(title_parser)
    def get(self):
        """
        Get movie titles in Berlin cinemas.
        """

        args = title_parser.parse_args()

        titles = db_accessor.read_distinct_movies(args['contains'])
        return titles
