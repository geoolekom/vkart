from django.views.generic import ListView

from posts.models import PostGroup


class PictureList(ListView):
    template_name = 'posts/picture_feed.html'
    model = PostGroup
    paginate_by = 10
    ordering = '-created',


class PictureBlock(ListView):
    template_name = 'posts/picture_block.html'
    model = PostGroup
    ordering = '-created',
    block_count = 10

    def get_queryset(self):
        generate = self.request.GET.get('generate')
        if generate:
            return self.generate_queryset()
        else:
            offset = self.request.GET.get('offset')
            return super().get_queryset()[offset:offset + self.block_count]

    def generate_queryset(self):
        pass
