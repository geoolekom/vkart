import vk
from parameters import vk_photo_sizes

def group_name_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]

def get_goods(url):
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
    if not 'attachment' in wall:
        return False, None
    if not 'photo' in wall['attachment']:
        return False, None
    if not 'attachments' in wall:
        return False, None

    post = {}
    post['like_count'] = wall['likes']['count']
    post['timestamp'] = wall['date']
    post['post_url'] = 'https://vk.com/wall{}?own=1&w=wall{}_{}'.format(wall['from_id'],
                                                                          wall['from_id'],
                                                                          wall['id'])
    attachment = wall['attachment']
    photo = attachment['photo']
    size_found = False
    for size in vk_photo_sizes:
        if size in photo:
            post['pic_url'] = photo[size]
            size_found = True
            break
    if not size_found:
        return False, None
    post['height'] = photo['height']
    post['width'] = photo['width']
    post['rating'] = 0.01
    return True, post
         	

def process_posts(walls):
    posts = []
    for wall in walls:
        success_process, post = create_post(wall)
        if success_process:
            posts.append(post) 
    return posts
