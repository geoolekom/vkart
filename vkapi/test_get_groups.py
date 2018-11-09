from parameters import user_token
from api import *
from pprint import pprint

api = get_api(user_token)
groups = get_groups(api, 98245887)

pprint(groups)