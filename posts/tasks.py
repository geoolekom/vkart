from django.contrib.auth import get_user_model

from posts.models import PublicGroup, Post
from vkapi.api import process_groups, get_best_pictures
from vkapi.group_ranker import rank_groups_for_user

USER_MODEL = get_user_model()


def get_best_posts(user_id):
    user = USER_MODEL.objects.filter(id=user_id)
    if user:
        api = user.get_api()
        uid = user.get_uid()

        group_ids = rank_groups_for_user(api, uid)
        groups = process_groups(api, group_ids)
        for group in groups:
            group_id = group.get('id')
            PublicGroup.objects.update_or_create(id=group_id, defaults=group)
            best_post_dicts = get_best_pictures(api, group_id)
            for post_dict in best_post_dicts:
                post_vk_id = post_dict.get('vk_id')
                Post.objects.update_or_create(vk_id=post_vk_id, group_id=group_id, defaults=post_dict)
