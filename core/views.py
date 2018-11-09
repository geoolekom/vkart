from django.urls import reverse
from django.views.generic import RedirectView


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('posts:picture_list')
        else:
            return reverse('accounts:login')
