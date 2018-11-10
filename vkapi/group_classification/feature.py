from .. import api as vkapi
from pprint import pprint
import re


class TfIdfContainer:
    model = None
    def __init__(self):
        pass


def text_process(s):
    return ' '.join(filter(lambda x: len(x) > 0, re.sub('[^a-zA-Zа-яА-Я ]', '', s.replace('\n', ' ').lower()).split(' ')))


def extract_text(api, group_id, **kwargs):
    texts = vkapi.get_group_texts(api, group_id, **kwargs)
    pprint(texts)
    res = []
    res.append(text_process(' '.join(texts['posts'])))
    res.append(text_process(' '.join(map(lambda x: x['title'] + ' ' + x['description'], texts['goods']))))
    res.append(text_process(' '.join(map(lambda x: x['title'] + ' ' + x['description'], texts['albums']))))
    return ' '.join(res)


if __name__ == '__main__':
    print(extract_text(vkapi.get_api(), '126622648', max_posts=100))
