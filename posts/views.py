import random
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView


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
                    'posts': list(set(chosen_posts))
                }
