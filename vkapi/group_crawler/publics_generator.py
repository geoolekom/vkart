import vk
import time
from .vkapi import api as vkapi
from group_recommendations import get_similar_groups


class UserStack(object):
    def __init__(self, api, seed_users):
        super(UserStack, self).__init__()
        self.api = api
        self.users = seed_users
        self.i = 0
    
    def extend_users(self):
        self.users.extend(vkapi.get_friends(self.api, self.users[self.i]))
        self.i += 1
    
    @staticmethod
    def make_seed_users():
        return []


class GroupGenerator(object):
    def __init__(self, api, seed_groups):
        self.api
        self.unseen_groups = set(seed_group)
        self.seen_groups = set()

    def __iter__(self):
        while len(self.unseen_seed_groups) > 0:
            group_id = self.unseen_groups.pop()
            self.seed_groups.add(group_id)
            similar_group_ids = set(get_similar_groups(self.api, group_id))
            unseen_similar_group_ids = similar_group_ids - self.seen_groups
            self.unseen_groups.update(unseen_similar_group_ids)
            if check_group_content(group_id):
                yield group_id
    
    def check_group_content(self, group_id):
        return True

