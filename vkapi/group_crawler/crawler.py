from .execute_database import *
from .recommendations import *
from .parameters import *
from time import sleep


def just_recommendations(api, public_id):
    session = vk.Session()
    api = vk.API(session)
    dbo = ExecuteDataBaseOperator(api, access_token, user_token, version)
    return get_recommendations(public_id, dbo, members_to_proceed=2000, top=100, output=True)


def generate_seed_groups():
    return ['126622648', '86082996', '129629677', '169672809', '98357630', '79748247', '141097690']


def groups_iterate(api, seed_groups):
    unseen_groups = set(seed_groups)
    stack_groups = set()
    seen_groups = set()

    while True:
        while len(unseen_groups) == 0:
            if len(stack_groups) == 0:
                return None 
            group_id = stack_groups.pop()
            seen_groups.add(group_id)
            try:
                similar_group_ids = set(map(lambda x: x['id'], just_recommendations(api, group_id)))
            except:
                sleep(2 * sleep_constant)
                try:
                    similar_group_ids = set(map(lambda x: x['id'], just_recommendations(api, group_id)))
                except:
                    continue

            unseen_similar_group_ids = similar_group_ids - seen_groups - stack_groups
            unseen_groups.update(unseen_similar_group_ids)
        
        group_id = unseen_groups.pop()
        stack_groups.add(group_id)
        yield group_id 



if __name__ == '__main__':
    for group_id in groups_iterate(None, generate_seed_groups()):
        print(group_id)
