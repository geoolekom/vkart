import vk
import vk.exceptions

import time

from parameters import vk_size_priorities


def handle_api_error(return_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except vk.exceptions.VkAPIError:
                return return_value
        return wrapper
    return decorator


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session, v='5.87')


def group_name_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]


def iterate_call(call, count, max_offset=None, **kwargs):
    if max_offset is None:
        max_offset = call(count=0, **kwargs)['count']

    for offset in range(0, max_offset, count):
        count = min(count, max_offset - offset)
        call_result = call(offset=offset, count=count, **kwargs)['items']
        time.sleep(0.4)
        for result in call_result:
            yield result


@handle_api_error([])
def get_friends(api, uid):
    return list(iterate_call(api.friends.get, 5000, user_id=uid))


@handle_api_error([])
def get_groups(api, uid):
    return list(iterate_call(
        lambda **kwargs: api.users.getSubscriptions(**kwargs)['groups'],
        200,
        user_id=uid)
    )


def get_group(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']

    posts = load_posts(api, group_id, 10, verbose=False)
    processed_posts = process_posts(posts, group_id)

    return {
        'url': url,
        'title': api.groups.getById(group_id=group_id)[0]['name'],
        'members': list(iterate_call(api.groups.getMembers, 1000, group_id=group_id)),
        'goods': list(iterate_call(api.market.get, 200, owner_id=-group_id)),
        'posts': processed_posts
    }

def get_group_posts(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']

    posts = load_posts(api, group_id, 10, verbose=False)
    processed_posts = process_posts(posts, group_id)

    return {
        'groups': [{
            'username': group_name,
            'id': group_id,
            'title': api.groups.getById(group_id=group_id)[0]['name']
        }],
        'posts': processed_posts
    }


def load_posts(api, community_id, count, offset = 0, verbose=True):
    current_offset = offset
    posts = []
    while current_offset < offset + count:
        try:
            if verbose:
                print('current_offset={}'.format(current_offset))
            wall = api.wall.get(
                owner_id=-community_id,
                offset=current_offset,
                count=100,
                filter='owner')['items']

            for item in wall:
                if isinstance(item, dict) and len(posts) < count:
                    posts.append(item)

            current_offset += 100
            time.sleep(0.2)
        except Exception as e:
            print('exception: {}'.format(str(e)))
            print('exception:(')
            pass

    return posts


class Photo:

    def __init__(self, post):
        self.likes = post['likes']['count']
        self.day = post['date'] / 86400
        self.second = post['date'] % 86400
        self.wall_link = 'https://vk.com/wall{}?own=1&w=wall{}_{}'.format(post['from_id'],
                                                                          post['from_id'],
                                                                          post['id'])
        attachment = post['attachment']
        photo = attachment['photo']
        sizes = ['src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big', 'src', 'src_small']
        for size in sizes:
            if size in photo:
                self.link = photo[size]
                break

    def __str__(self):
        return 'likes={}'.format(self.likes) + \
               '\nday={}'.format(self.day) + \
               '\nsecond={}'.format(self.second) + \
               '\nlink={}'.format(self.link) + \
               '\nwall_link={}'.format(self.wall_link)


def create_post(wall):
    if not 'attachments' in wall:
        return False, None
    attachment = wall['attachments'][0]
    if not 'photo' in attachment:
        return False, None
    post = {}
    post['like_count'] = wall['likes']['count']
    post['timestamp'] = wall['date']
    post['post_url'] = 'https://vk.com/wall{}?own=1&w=wall{}_{}'.format(wall['from_id'],
                                                                          wall['from_id'],
                                                                          wall['id'])
    photo = attachment['photo']
    best_size = photo['sizes'][0]
    best_type = best_size['type']
    for size in photo['sizes']:
        if vk_size_priorities[size['type']] < vk_size_priorities[best_type]:
            best_size = size
            best_type = size['type']
    post['text'] = wall['text']
    post['pic_url'] = best_size['url']
 
    post['height'] = best_size['height']
    post['width'] = best_size['width']
    post['rating'] = 0.01
    post['id'] = wall['id']
    return True, post


def process_posts(walls, group_id):
    posts = []
    for wall in walls:
        success_process, post = create_post(wall)
        if success_process:
            post['group_id'] = group_id
            posts.append(post) 

    return posts
