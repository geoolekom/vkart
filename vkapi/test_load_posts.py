from api import load_posts
from parameters import user_token, version
from pprint import pprint
import vk

session = vk.Session()
api = vk.API(session)

community_id = 126622648

posts = load_posts(api, community_id, 20, user_token, version)
print('posts loaded!')

for post in posts:
	pprint(post)
	print('-----------------')