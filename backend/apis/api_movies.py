""""
Includes the endpoints for namespace movies
"""

from flask_restplus import Namespace, Resource, reqparse

from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

search_parser = reqparse.RequestParser()
search_parser.add_argument(name='contains',
                           required=False,
                           help='substr to be contained in the title')

api = Namespace('movies',
                description='Retrieve information about movies.')


@api.route('/titles')
class Movies(Resource):

    @api.expect(search_parser)
    def get(self):
        """
        Retrieve movie titles in Berlin cinemas
        """

        args = search_parser.parse_args()

        titles = db_accessor.read_distinct_movies(args['contains'])
        return titles
