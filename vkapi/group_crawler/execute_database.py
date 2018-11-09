from .loading_functions import execute_get_communities, get_community_size, get_distributed_ids, get_ids, get_community_sizes, current_milli_time
import threading
from collections import Counter
import time
lock = threading.Lock()

def parallel_get_communities(thread_name, user_ids, threshold, dbo):
    cur_user_subscrs, cur_id_to_name, cur_id_to_link = \
                execute_get_communities(
                                user_ids,
                                70,
                                dbo.api,
                                dbo.access_token,
                                dbo.user_token,
                                dbo.version,
                                dbo)
    global lock
    with lock:
        for k, v in cur_id_to_name.items():
            dbo.id_to_name[k] = v
        for k, v in cur_id_to_link.items():
            dbo.id_to_link[k] = v
        for user, subscrs in cur_user_subscrs.items():
            for _, community in enumerate(subscrs[:threshold]):
                dbo.communities[community] += 1



class ExecuteDataBaseOperator():

    def __init__(self, api, access_token, user_token, version):
        self.api = api
        self.version = version
        self.access_token = access_token
        self.user_token = user_token
        self.id_to_name = {}
        self.id_to_link = {}

    def get_community_size(self, community_id):
        return get_community_size(community_id,
                                  self.api,
                                  self.access_token,
                                  self.version)

    def get_distributed_ids(self, community_id):
        return get_distributed_ids(community_id,
                                   self.api,
                                   self.access_token,
                                   self.version)

    def get_ids(self, community_id):
        return get_ids(community_id,
                       self.api,
                       self.access_token,
                       self.version)

    def parallel_get_communities(self, user_ids, threshold):

        self.prev_milli = -1
        self.communities = Counter()

        threads = []
        for i in range(0, len(user_ids) - 1, 25):
            threads.append(
                threading.Thread(
                    target=parallel_get_communities,
                    args=('thread{}'.format(i),
                          user_ids[i : min(i + 25, len(user_ids))],
                          threshold,
                          self)))

        for i, thread in enumerate(threads):
            if i % 15 == 0:
                print('{} members processed'.format(25 * i))
            time.sleep(max(0.35 - (current_milli_time() - self.prev_milli) / 1000.0, 0.0))
            thread.start()

        for thread in threads:
            thread.join()

        return self.communities


    def get_communities(self, user_ids, threshold, dbo):
        prev_milli = -1
        id_to_name = {}
        id_to_link = {}
        communities = Counter()
        for i in range(0, len(user_ids) - 1, 25):
            if i % 100 == 0:
                print('{} members processed'.format(100 * i))
            time.sleep(max(0.3334 - (current_milli_time() - prev_milli) / 1000.0, 0.0))
            prev_milli = current_milli_time()
            user_subscrs, id_to_name, id_to_link = \
                execute_get_communities(
                                user_ids[i : min(i + 25, len(user_ids))],
                                70,
                                self.api,
                                self.access_token,
                                self.user_token,
                                self.version,
                                dbo)
            for k, v in id_to_name.items():
                self.id_to_name[k] = v
            for k, v in id_to_link.items():
                self.id_to_link[k] = v
            for user, subscrs in user_subscrs.items():
                for _, community in enumerate(subscrs[:threshold]):
                    communities[community] += 1
        return communities

    def get_community_sizes(self, community_ids):
        return get_community_sizes(community_ids, self.api, self.access_token, self.version)

    def get_community_name(self, id):
        return self.id_to_name[id]

    def get_community_link(self, id):
        return self.id_to_link[id]
