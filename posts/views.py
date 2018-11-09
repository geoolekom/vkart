from django.views.generic import ListView

from posts.models import Post


class PictureList(ListView):
    template_name = 'posts/feed.html'
    model = Post
    paginate_by = 10

