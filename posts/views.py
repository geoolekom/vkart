from django.views.generic import ListView

from posts.models import PostGroup


class PictureList(ListView):
    template_name = 'posts/feed.html'
    model = PostGroup
    paginate_by = 10
    ordering = '-created',
