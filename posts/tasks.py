from datetime import datetime

import pytz
from project.celery import app
from django.conf import settings
from django.contrib.auth import get_user_model

from posts.models import PublicGroup, Post, UserGroup
from vkapi.api import process_groups, get_best_pictures
from vkapi.group_ranker import rank_groups_for_user

USER_MODEL = get_user_model()


@app.task
def update_best_posts(user_id):
    user = USER_MODEL.objects.filter(id=user_id).first()
    if user:
        api = user.get_api()
        uid = user.get_uid()

        if uid and api:
            print('Обновляем пользователя {0}'.format(uid))
            group_dict_list = rank_groups_for_user(api, uid)
            group_ids = [group_dict.get('id') for group_dict in group_dict_list]
            groups = process_groups(api, group_ids)
            for group_dict in group_dict_list:
                group_id = group_dict.get('id')
                group = groups.get(group_id)
                if group:
                    group, _ = PublicGroup.objects.update_or_create(id=group_id, defaults=group)
                    UserGroup.objects.update_or_create(user_id=user_id, group=group,
                                                       defaults={'rating': group_dict.get('rating', 0.01)})
                print('Обновлена группа {0}'.format(group_id))
            print('-----')

            for group_id, group in groups.items():
                best_post_dicts = get_best_pictures(api, group_id)
                for post_dict in best_post_dicts:
                    post_vk_id = post_dict.get('vk_id')
                    timestamp = post_dict.get('timestamp')
                    timestamp = datetime.fromtimestamp(timestamp, pytz.timezone(settings.TIME_ZONE))
                    post_dict['timestamp'] = timestamp
                    Post.objects.update_or_create(vk_id=post_vk_id, group_id=group_id, defaults=post_dict)
                print('Загружены посты из группы {0}'.format(group_id))
            print('-----\nВыполнено.')


@app.task
def update_all():
    for user in USER_MODEL.objects.all():
        update_best_posts(user.id)
