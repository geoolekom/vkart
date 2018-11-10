from .. import api as vkapi
from pprint import pprint
import re


def text_process(s):
    return ' '.join(filter(lambda x: len(x) > 0, re.sub('[^a-zA-Zа-яА-Я ]', '', s.replace('\n', ' ').lower()).split(' ')))


def extract_features(api, group_id, **kwargs):
    texts = vkapi.get_group_texts(api, group_id, **kwargs)
    return text_process(' '.join(texts['posts']))


if __name__ == '__main__':
    print(extract_features(vkapi.get_api(), '126622648', max_posts=100))
