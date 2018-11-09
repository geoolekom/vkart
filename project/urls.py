from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from core.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', IndexView.as_view(), name='index'),
    path('', include('posts.urls', namespace='posts')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[
        path('__debug__/', include(debug_toolbar.urls)),
    ]
