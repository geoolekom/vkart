from .execute_database import *
from .recommendations import *
from .parameters import *
 
def just_recommendations(api, public_id):
    session = vk.Session()
    api = vk.API(session)
    dbo = ExecuteDataBaseOperator(api, access_token, user_token, version)
    return get_recommendations(public_id, dbo, members_to_proceed=200, top=100, output=True)


def generate_seed_groups():
    return []


def groups_iterate(api, group_id, seed_groups):
    unseen_groups = set(seed_groups)
    seen_groups = set()

    while len(unseen_groups) > 0:
        group_id = unseen_groups.pop()
        similar_group_ids = set(map(lambda x: x['id'], just_recommendations(api, groups_id)))
        unseen_similar_group_ids = similar_group_ids - seen_groups
        unseen_groups.update(unseen_similar_group_ids)
        seen_groups.add(group_id)
        yield group_id

