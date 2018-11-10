from .api import *
from pprint import pprint

api = get_api()
friends = get_friends(api, 98245887)

pprint(friends)
