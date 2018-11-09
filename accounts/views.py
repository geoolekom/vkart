from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    http_method_names = ['get']
    next_page = reverse_lazy('accounts:login')


class LoginView(BaseLoginView):
    http_method_names = ['get', 'post']
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        url = super().get_redirect_url()
        if url:
            return url
        else:
            return reverse('posts:picture_list')
