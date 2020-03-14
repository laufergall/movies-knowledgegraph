""""
Puts together the API namespaces
"""

from flask_restplus import Api

from .api_cinemas import api as api_c
from .api_movies import api as api_m

api = Api(version='1.0',
          default='movies',
          title='Kinoprogramm',
          description='Check out which movies are playing and where in Berlin cinemas.')

api.namespaces.clear()
api.add_namespace(api_m)
api.add_namespace(api_c)
