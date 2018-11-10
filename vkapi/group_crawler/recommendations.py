import vk
import time
from .statistics import relation
import random

def get_recommendations(community_id,
                        dbo,
                        members_to_proceed=300,
                        most_common=500,
                        top=100,
                        output=False):
    # potential Exception
    start = int(round(time.time() * 1000))
    N, ids = dbo.get_distributed_ids(community_id)
    finish = int(round(time.time() * 1000))
    # print('N = {}'.format(N))
    # print('dbo.get_distributed_ids time:{}'.format(finish - start))
    ids.sort()

    random.shuffle(ids)

    # if output:
    #     print('members_to_proceed = {}'.format(members_to_proceed))
    start = int(round(time.time() * 1000))
    communities = dbo.parallel_get_communities(ids[:min(len(ids), members_to_proceed)], 40)
    finish = int(round(time.time() * 1000))
    # print('dbo.get_communities time:{}'.format(finish - start))
    # print('mined communities: {}'.format(len(communities)))
    popular_communities = communities.most_common(most_common)

    community_sizes = {}
    community_ids = [item[0] for item in popular_communities]

    for id, size in dbo.get_community_sizes(community_ids):
        community_sizes[id] = size

    popular_communities.sort(key = lambda x: relation(x[1], community_sizes[x[0]]), reverse=True)

    recommended_communities = []
    for item in popular_communities[:top]:
        community_size = community_sizes[item[0]]
        rel = relation(item[1], community_sizes[item[0]])
        recommended_communities.append(
            {'id' : item[0],
             'link': dbo.get_community_link(item[0]),
             'name' : dbo.get_community_name(item[0]),
             'common' : item[1],
             'size' : community_size,
             'rank' : 100 * rel * N / members_to_proceed})
    return recommended_communities

def get_rank(community_id, recommendations):
    for i, r in enumerate(recommendations):
        if r['id'] == community_id:
            return i
    return None

if __name__ == '__main__':  
    session = vk.Session()
    api = vk.API(session)

    dbo = DataBaseOperator(api, access_token, version)
    database_address = 'database.txt'
    dbo.load(database_address)

    recommendations = get_recommendations(community_id,
                                          dbo,
                                          members_to_proceed=members_to_proceed,
                                          top=100,
                                          output=True)
    for i, r in enumerate(recommendations):
        print('{} {} {} {} {}'.format(r['link'], r['name'], r['common'], r['size'], r['rank']))

    for i, r in enumerate(recommendations):
        print('{} {} {} {} {}'.format(r['link'], r['name'], r['common'], r['size'], r['rank']))
        sub_recommendations = get_recommendations(r['id'],
                                                  dbo,
                                                  members_to_proceed = 300,
                                                  top=100)
        rank = get_rank(community_id, sub_recommendations)
        print('rank = {}'.format(rank))
        dbo.dump(database_address)
