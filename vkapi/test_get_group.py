from parameters import user_token
from api import *
from pprint import pprint

api = get_api(user_token)
group = get_group(api, 'https://vk.com/narwhalart')

pprint(group)
