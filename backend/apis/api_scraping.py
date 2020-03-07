""""
Includes the endpoints for namespace1
"""

from flask_restplus import Namespace, Resource

api = Namespace('scraping',
                description='Retrieve cinema program.')


@api.route('/movies')
class Movies(Resource):

    def get(self):
        """
        Retrieve movies in Berlin cinemas
        """

        return 'TODO'
