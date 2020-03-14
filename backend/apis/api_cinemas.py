""""
Includes the endpoints for namespace cinamas
"""

from flask_restplus import Namespace, Resource, reqparse
from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

names_parser = reqparse.RequestParser()
names_parser.add_argument(name='contains',
                          default='',
                          required=False,
                          help='substr to be contained in the cinema name')

times_parser = reqparse.RequestParser()
times_parser.add_argument(name='cinema_contains',
                          default='',
                          required=False,
                          help='substr to be contained in the cinema name')
times_parser.add_argument(name='title_contains',
                          default='',
                          required=False,
                          help='substr to be contained in the movie title')

api = Namespace('cinemas',
                description='Retrieve information about cinemas and currently playing movies.')


@api.route('/names')
class CinemaNames(Resource):

    @api.expect(names_parser)
    def get(self):
        """
        Get Berlin cinema names.
        """

        args = names_parser.parse_args()

        cinemas = db_accessor.read_distinct_cinemas(args['contains'])
        return cinemas


@api.route('/movie_times')
class MovieTimes(Resource):
    """
    Get cinemas where movie is playing along with show times.
    """

    @api.expect(times_parser)
    def get(self):
        args = times_parser.parse_args()

        cinemamovies = db_accessor.read_showtimes(args['cinema_contains'],
                                                  args['title_contains'])
        return [cn.to_dict() for cn in cinemamovies]
