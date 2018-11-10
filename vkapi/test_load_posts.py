from .api import load_posts, process_posts
from .parameters import version, access_token
from pprint import pprint
import vk

session = vk.Session()
api = vk.API(session)

community_id = 126622648

posts = load_posts(api, community_id, 5, access_token, version)
print('posts loaded!')

for post in posts:
    pprint(post)
    print('-----------------')

processed_posts = process_posts(posts, community_id)

for post in processed_posts:
    pprint(post)
    print('-----------------')

