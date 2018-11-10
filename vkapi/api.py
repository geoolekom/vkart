import vk
import vk.exceptions

import logging
import time

try:
    from .ratings import set_ratings
except ImportError:
    from ratings import set_ratings

try:
    from .parameters import vk_size_priorities, access_token, version
except ImportError:
    from parameters import vk_size_priorities, access_token, version


def handle_api_error(return_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except vk.exceptions.VkAPIError:
                return return_value
        return wrapper
    return decorator


def get_api():
    session = vk.Session(access_token=access_token)
    return vk.API(session, v=version)


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


@handle_api_error([])
def get_group_goods(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']
    return list(iterate_call(api.market.get, 200, owner_id=-group_id))


@handle_api_error([])
def get_group_albums(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']
    return api.photos.getAlbums(owner_id=-group_id)['items']


def get_group_texts(api, url, max_posts=1e6):
    group_name = group_name_from_url(url)
    group_info = api.groups.getById(group_id=group_name, fields='status,description')[0]
    id = group_info['id']

    posts = get_group_posts(api, url, max_posts)['posts']

    return {
        'url': 'vk.com/{}'.format(group_info['screen_name']),
        'username': group_info['name'],
        'title': group_info['screen_name'],
        'description': group_info['description'],
        'status': group_info['status'],
        'posts': list(map(lambda post: post['text'], posts)),

        'albums': list(
            map(
                lambda album: {
                    'title': album['title'],
                    'description': album['description']
                },
                get_group_albums(api, url)
            )),

        'goods': list(
            map(
                lambda good: {
                    'title': good['title'],
                    'description': good['description'],
                },
                get_group_goods(api, url))
        )
    }


def get_group(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']

    posts = load_posts(api, group_id, 10, verbose=False)
    processed_posts = process_posts(posts)

    return {
        'url': url,
        'title': api.groups.getById(group_id=group_id)[0]['name'],
        'members': list(iterate_call(api.groups.getMembers, 1000, group_id=group_id)),
        'goods': list(iterate_call(api.market.get, 200, owner_id=-group_id)),
        'posts': processed_posts
    }


def get_group_posts(api, url, max_posts=1e6):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']

    posts = load_posts(api, group_id, max_posts, verbose=False)
    processed_posts = process_posts(posts)

    return {
        'groups': [{
            'username': group_name,
            'id': group_id,
            'title': api.groups.getById(group_id=group_id)[0]['name']
        }],
        'posts': processed_posts
    }


def load_posts(api, community_id, count, offset=0, verbose=True):
    current_offset = offset
    posts = []
    while current_offset < offset + count:
        try:
            if verbose:
                logging.info('current_offset={current_offset}')
            wall = api.wall.get(
                owner_id=-community_id,
                offset=current_offset,
                count=100,
                filter='owner')['items']

            for item in wall:
                if isinstance(item, dict) and len(posts) < count:
                    posts.append(item)

            current_offset += 100
        except Exception as e:
            logging.error(e, exc_info=True)
        finally:
            time.sleep(0.2)

    return posts


class Photo(object):

    def __init__(self, post):
        self.likes = post['likes']['count']
        self.day = post['date'] / 86400
        self.second = post['date'] % 86400
        self.wall_link = f'https://vk.com/wall{post["from_id"]}_{post["id"]}'

        attachment = post['attachment']
        photo = attachment['photo']
        sizes = ['src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big', 'src', 'src_small']
        for size in sizes:
            if size in photo:
                self.link = photo[size]
                break

    def __str__(self):
        return f'likes={self.likes}\nday={self.day}\nsecond={self.second}\nlink={self.link}\nwall_link={self.wall_link}'


def create_post(wall):
    if 'attachments' not in wall:
        return False, None
    attachment = wall['attachments'][0]
    if 'photo' not in attachment:
        return False, None

    photo = attachment['photo']
    best_size = photo['sizes'][0]
    best_type = best_size['type']
    for size in photo['sizes']:
        if vk_size_priorities[size['type']] < vk_size_priorities[best_type]:
            best_size = size
            best_type = size['type']

    return True, {
        'id': wall['id'],
        'like_count': wall['likes']['count'],
        'timestamp': wall['date'],
        'post_url': 'https://vk.com/wall'.format(wall["from_id"], wall["id"]),
        'text': wall['text'],
        'pic_url': best_size['url'],
        'height': best_size['height'],
        'width': best_size['width'],
        'rating': 0.01,
        'group_id': - wall['from_id']
    }


def process_groups(api, group_ids):
    api_groups = api.groups.getById(group_ids=group_ids)
    return [{'id': group['id'], 'screen_name': group['screen_name'], 'title': group['name']} for group in api_groups]


def process_posts(api_posts):
    posts = []
    for post in api_posts:
        success, post_dict = create_post(post)
        if success:
            posts.append(post_dict)
    return posts


def get_posts(api, group_ids: list):
    groups = process_groups(api, group_ids)
    posts = []
    for group in groups:
        group_id = group['id']
        api_posts = load_posts(api, group_id, 10, verbose=False)
        posts = process_posts(api_posts)

    return {
        'groups': groups,
        'posts': posts
    }


def get_best_pictures(api, group_id):
    posts = load_posts(api, group_id, 500, verbose=False)
    processed_posts = process_posts(posts)
    set_ratings(processed_posts)
    return [post for post in processed_posts if post['rating'] > 0.95]


