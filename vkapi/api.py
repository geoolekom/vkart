import vk

def get_api(access_token):
    session = vk.Session(access_token=access_token)
    api = vk.API(session, v='5.87')

def group_name_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]

def get_goods(api, url):
    owner_name = group_name_from_url(url)
    owner_id = api.groups.getById(group_id=owner_name)[0]['id']
    return api.market.get(owner_id=-owner_id)

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
