from .. import api as vkapi
from .. import group_crawler
from .. import parameters
from time import sleep


def generate_data(api, path):
    with open(path, 'w') as f:
        f.write('group_id,group_url,label')
        for group_id in group_crawler.crawler.groups_iterate(api, group_crawler.crawler.generate_seed_groups()):
            f.write('%s,%s,' % (group_id, vkapi.get_group_url(api, group_id)))
            sleep(parameters.sleep_constant)


if __name__ == '__main__':
    generate_data(vkapi.get_api(), './train.csv')
