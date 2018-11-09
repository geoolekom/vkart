from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[
        path('__debug__/', include(debug_toolbar.urls)),
    ]
