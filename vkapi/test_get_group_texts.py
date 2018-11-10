from .parameters import access_token
from .api import *
from pprint import pprint

api = get_api()
texts = get_group_texts(api, 'fr01ik', 10)

pprint(texts)