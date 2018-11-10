try:
    from .api import *
except Exception: #ImportError
    from api import *

from pprint import pprint
import vk

api = get_api()

community_id = 126622648

posts = get_best_pics(api, community_id)

for post in posts:
	pprint(post)