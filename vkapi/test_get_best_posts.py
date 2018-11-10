try:
    from .api import *
except Exception as e:
    from api import *

from pprint import pprint

api = get_api()

community_id = 126622648

posts = get_best_pictures(api, community_id)

for post in posts:
	print(post['like_count'], post['rating'], post['pic_url'])
