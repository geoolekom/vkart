from posts.views import PictureList, OldPictureBlock, NewPictureBlock, RandomPictureBlock

from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('pictures/', PictureList.as_view(), name='picture_list'),
    path('pictures/old/', OldPictureBlock.as_view(), name='old_picture_block'),
    path('pictures/new/', NewPictureBlock.as_view(), name='new_picture_block'),
    path('pictures/random/', RandomPictureBlock.as_view(), name='random_picture_block'),
]
