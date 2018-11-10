import time
import random

current_milli_time = lambda: int(round(time.time() * 1000))


def get_community_sizes(id_list, api, access_token, version):
    for i in range(0, len(id_list), 500):
        result = api.groups.getById(
            group_ids=','.join([str(id) for id in id_list[i:min(i+500, len(id_list))]]),
            access_token=access_token,
            v=version,
            fields=['members_count'])
        for item in result:
            yield item['id'], item['members_count']

def get_community_size(community_id, api, access_token, version):
    tries = 0
    while True:
        time.sleep(0.1)
        try:
            return api.groups.getMembers(
                    group_id=community_id,
                    offset=0,
                    count=0,
                    access_token=access_token,
                    v=version)['count']
        except Exception as e:
            print('in get_community_size:')
            print(e)
            tries += 1
            if tries > 3:
                raise Exception(e)

def get_distributed_ids(community_id, api, access_token, version, limit=50000):
    count = get_community_size(community_id, api, access_token, version)
    chunk_length = 1000
    member_reading_limit = chunk_length
    chunks = [i for i in range(0, count // chunk_length + 1)]
    random.shuffle(chunks)
    chunks = chunks[:min(len(chunks), limit // chunk_length + 1)]
    print('chunks={}'.format(chunks))
    ids = []
    tries = 0
    for chunk in chunks:
        offset = chunk_length * chunk
        try:
            members = api.groups.getMembers(
                    group_id=community_id,
                    offset=offset,
                    count=member_reading_limit,
                    access_token=access_token,
                    v=version
            )
            ids += members['items']
            time.sleep(0.06)
        except Exception as e:
            print('exception in get_ids: {}'.format(e))
            tries += 1
            if tries > 3:
                raise Exception(e)
            pass
    return count, ids


def get_ids(community_id, api, access_token, version, limit=10000):
    count = get_community_size(community_id, api, access_token, version)
    if limit > 0:
        count = limit
    member_reading_limit = 1000
    current_offset = 0
    ids = []
    tries = 0
    while current_offset < count:
        print('current_offset={}'.format(current_offset))
        try:
            members = api.groups.getMembers(
                    group_id=community_id,
                    offset=current_offset,
                    count=member_reading_limit,
                    access_token=access_token,
                    v=version
            )
            ids += members['items']
            current_offset += member_reading_limit
            time.sleep(0.4)
        except Exception as e:
            print('exception in get_ids: {}'.format(e))
            tries += 1
            if tries > 3:
                raise Exception(e)
            pass
    return count, ids

def get_communities(user_id, threshold, api, access_token, version):
    id_to_name = {}
    id_to_link = {}
    while True:
        try:
            time.sleep(0.055)
            communities = api.users.getSubscriptions(
                    user_id=user_id,
                    offset=0,
                    count=threshold,
                    access_token=access_token,
                    v=version,
                    fields=['id', 'name', 'screen_name'],
                    extended=True
                )
            subscrs = []
            for item in communities['items']:
                if 'id' in item.keys() and 'name' in item.keys():
                    id_to_name[item['id']] = item['name']
                    id_to_link[item['id']] = 'vk.com/' + item['screen_name']
                    subscrs.append(item['id'])

            return subscrs, id_to_name, id_to_link
        except Exception as e:
            if str(e) != 'name':
                print('exception: {}'.format(e))
            return [], {}

def execute_get_communities(user_ids,
                            threshold,
                            api,
                            access_token,
                            user_token,
                            version,
                            dbo):
    id_to_name = {}
    id_to_link = {}
    vk_script_code = 'return ['
    for user_id in user_ids:
        pattern = 'API.users.getSubscriptions({' + \
                  '"user_id" : {} , '.format(user_id) + \
                  '"access_token" : "{}", '.format(access_token) + \
                  '"count" : {}, '.format(threshold) + \
                  '"v" : "{}", '.format(version) + \
                  '"fields" : ["id", "name", "screen_name"], ' + \
                  '"extended" : 1}), '
        vk_script_code += pattern
    vk_script_code += '];'
    try:
        dbo.prev_milli = current_milli_time()
        user_communities = api.execute(code=vk_script_code,
                                       access_token=user_token,
                                       v=version)
    except Exception as e:
        print('execute_get_communities:exceptions:{}'.format(str(e)[:40]))
        return {}, {}, {}

    user_subscrs = {}

    for user, communities in zip(user_ids, user_communities):
        subscrs = []
        if not isinstance(communities, dict):
            continue
        for item in communities['items']:
            if 'id' in item.keys() and 'name' in item.keys():
                id_to_name[item['id']] = item['name']
                id_to_link[item['id']] = 'vk.com/' + item['screen_name']
                subscrs.append(item['id'])

        user_subscrs[user] = subscrs
    return user_subscrs, id_to_name, id_to_link
