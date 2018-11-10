from collections import defaultdict

import random
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from posts.models import PostGroup, PublicGroup, Post
from vkapi.api import get_best_pictures, process_groups
from vkapi.group_ranker import rank_groups_for_user


class PictureList(LoginRequiredMixin, TemplateView):
    template_name = 'posts/picture_feed.html'


class RandomPictureBlock(LoginRequiredMixin, ListView):
    template_name = 'posts/picture_block.html'
    post_count = 5
    group_count = 10

    def get_queryset(self):
        user = self.request.user
        user_groups = user.usergroup_set.all()
        group_weights = user_groups.values_list('rating', flat=True)
        chosen_groups = random.choices(user_groups, weights=group_weights, k=self.group_count)
        for user_group in chosen_groups:
            group_posts = user_group.group.post_set.all()
            if group_posts.count():
                post_weights = group_posts.values_list('rating', flat=True)
                chosen_posts = random.choices(group_posts, weights=post_weights, k=self.post_count)
                yield {
                    'id': str(uuid.uuid4()),
                    'group': user_group.group,
                    'posts': chosen_posts
                }


class NewPictureBlock(LoginRequiredMixin, ListView):
    template_name = 'posts/picture_block.html'
    model = PostGroup
    ordering = '-created',
    post_count = 5

    def get_queryset(self):
        user = self.request.user
        api = user.get_api()
        group_ids = rank_groups_for_user(api, user.get_uid())
        groups = process_groups(api, group_ids)
        new_posts = defaultdict(list)
        for group in groups:
            group_id = group.get('id')
            PublicGroup.objects.update_or_create(id=group_id, defaults=group)
            best_post_dicts = get_best_pictures(api, group_id)
            for post_dict in best_post_dicts:
                post_vk_id = post_dict.get('vk_id')
                post, created = Post.objects.update_or_create(vk_id=post_vk_id, group_id=group_id, defaults=post_dict)
                if created:
                    new_posts[group_id].append(post)

        offset = 0
        post_groups = []
        while True:
            pg_created = False
            for group_id, post_list in new_posts.items():
                current_slice = post_list[offset:offset + self.post_count]
                if len(current_slice) > 3:
                    pg_created = True
                    pg = PostGroup.objects.create(user=user, group_id=group_id)
                    pg.posts.set(current_slice)
                    post_groups.append(pg)
            offset += self.post_count
            if not pg_created:
                break
        return reversed(post_groups)


class OldPictureBlock(LoginRequiredMixin, ListView):
    template_name = 'posts/picture_block.html'
    model = PostGroup
    ordering = '-created',
    block_count = 10

    def get_queryset(self):
        user = self.request.user
        offset = self.request.GET.get('offset', '0')
        queryset = PostGroup.objects.filter(user=user)
        if offset and offset.isdigit():
            offset = int(offset)
            return queryset[offset * self.block_count:(offset + 1) * self.block_count]
        else:
            return queryset[:self.block_count]
