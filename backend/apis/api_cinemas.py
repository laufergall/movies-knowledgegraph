""""
Includes the endpoints for namespace cinamas
"""

from flask_restplus import Namespace, Resource

from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

api = Namespace('cinemas',
                description='Retrieve information about cinemas and currently playing movies.')


@api.route('/names')
class CinemaNames(Resource):

    def get(self):
        """
        Get Berlin cinema names
        """

        return {'TODO': 'Task 3'}
