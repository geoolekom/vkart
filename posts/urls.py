from posts.views import PictureList, RandomPictureBlock

from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('pictures/', PictureList.as_view(), name='picture_list'),
    path('pictures/random/', RandomPictureBlock.as_view(), name='random_picture_block'),
]
