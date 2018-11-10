from .. import api as vkapi
from .. import group_crawler
from .. import parameters
from time import sleep


def generate_data(api, path):
    with open(path, 'w') as f:
        f.write('group_id,group_url,label\n')
        for group_id in group_crawler.crawler.groups_iterate(api, group_crawler.crawler.generate_seed_groups()):
            try:
                group_url = vkapi.get_group_url(api, group_id)
            except:
                sleep(2 * parameters.sleep_constant)
                try:
                    group_url = vkapi.get_group_url(api, group_id)
                except:
                    continue
            
            f.write('%s,%s,\n' % (group_id, group_url))
            f.flush()
            sleep(parameters.sleep_constant)


if __name__ == '__main__':
    generate_data(vkapi.get_api(), './train.csv')
