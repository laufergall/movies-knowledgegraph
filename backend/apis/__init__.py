""""
Puts together the API namespaces
"""

from flask_restplus import Api

from .api_scraping import api as api_s

api = Api(version='1.0',
          default='scraping',
          title='Kinoprogramm',
          description='Retrieve the current cinema program and check out which movies are playing and where.')

api.namespaces.clear()
api.add_namespace(api_s)
