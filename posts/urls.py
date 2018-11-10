from posts.views import PictureList, RandomPictureBlock, GenrePictureList, GenreRandomPictureBlock, TogglePostLike

from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('toggle_like/', TogglePostLike.as_view(), name='toggle_like'),
    path('pictures/', PictureList.as_view(), name='picture_list'),
    path('pictures/random/', RandomPictureBlock.as_view(), name='random_picture_block'),

    path('<slug:slug>/', GenrePictureList.as_view(), name='genre_picture_list'),
    path('<slug:slug>/random/', GenreRandomPictureBlock.as_view(), name='genre_random_picture_block'),
]
