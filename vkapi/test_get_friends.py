from parameters import user_token
from api import *
from pprint import pprint

api = get_api(user_token)
friends = get_friends(api, 98245887)

pprint(friends)
