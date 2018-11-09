import vk
import time


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    api = vk.API(session, v='5.87')


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


def get_group(api, url):
    group_name = group_name_from_url(url)
    group_id = api.groups.getById(group_id=group_name)[0]['id']

    return {
        'url': url,
        'title': api.groups.getById(group_id=group_id)[0]['name'],
        'members': list(iterate_call(api.groups.getMembers, 1000, group_id=group_id)),
        'goods': list(iterate_call(api.market.get, 200, owner_id=-group_id))
    }


def load_posts(api, community_id, count, user_token, version, offset = 0, verbose=True):
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
                filter='owner',
                access_token=user_token,
                version=version
            )

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
