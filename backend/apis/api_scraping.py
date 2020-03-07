""""
Includes the endpoints for namespace1
"""

from flask_restplus import Namespace, Resource

api = Namespace('scraping',
                description='Retrieve cinema program.')


@api.route('/berlin')
class Endpoint1(Resource):

    def get(self):
        """
        docstr GET
        """

        return 'Hello - minimal flask restplus'
