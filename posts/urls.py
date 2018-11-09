from posts.views import PictureList

from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('pictures/', PictureList.as_view(), name='picture_list'),
]
