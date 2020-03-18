""""
Includes the endpoints for namespace cinamas
"""

from flask_restplus import Namespace, Resource, reqparse

from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

name_parser = reqparse.RequestParser()
name_parser.add_argument(name='cinema_contains',
                         default='',
                         required=False,
                         help='substr to be contained in the cinema name')

title_parser = reqparse.RequestParser()
title_parser.add_argument(name='title_contains',
                          default='',
                          required=False,
                          help='substr to be contained in the movie title')

exact_name_parser = reqparse.RequestParser()
exact_name_parser.add_argument(name='name',
                               required=True,
                               help='exact cinema name')

api = Namespace('cinemas',
                description='Retrieve information about cinemas and currently playing movies.')


@api.route('/names')
class CinemaNames(Resource):

    @api.expect(name_parser)
    def get(self):
        """
        Get Berlin cinema names
        """

        return {'TODO (Task 3)'}
