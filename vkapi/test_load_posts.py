try:
    from .api import load_posts, process_posts, get_api
except Exception as e:
    from api import load_posts, process_posts, get_api

from pprint import pprint
import vk

api = get_api()

community_id = 126622648

posts = load_posts(api, community_id, 1000)
print('posts loaded!')

for post in posts:
	pass
    # pprint(post)
    # print('-----------------')

processed_posts = process_posts(posts)
print(len(processed_posts))
exit(0)
for post in processed_posts:
    pprint(post)
    print('-----------------')

