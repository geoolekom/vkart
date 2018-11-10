from .api import *
from pprint import pprint

api = get_api()
groups = get_groups(api, 98245887)

pprint(groups)
