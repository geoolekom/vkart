try:
  from .parameters import access_token
except:
  from parameters import access_token

try:
  from .api import *
except:
  from api import *
from pprint import pprint

api = get_api()
#texts = get_group_texts(api, 'jumoreski', 10)
print(get_group_url(api, 136765630))

#pprint(texts)
