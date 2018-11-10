from .api import *
from pprint import pprint

api = get_api()
group = get_group_posts(api, 'https://vk.com/narwhalart')

pprint(group)
