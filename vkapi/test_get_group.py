from .api import *
from pprint import pprint

api = get_api()
group = get_group(api, 'https://vk.com/narwhalart')

pprint(group)
