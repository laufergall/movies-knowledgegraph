""""
Includes the endpoints for namespace cinamas
"""

from flask_restplus import Namespace, Resource
from .db_access import MongoDBConnector


db_accessor = MongoDBConnector()

api = Namespace('cinemas',
                description='Retrieve information about cinemas and currently playing movies.')


@api.route('/names')
class Cinemas(Resource):

    def get(self):
        cinemas = db_accessor.read_distinct_cinemas()
        return cinemas
