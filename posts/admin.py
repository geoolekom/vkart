from django.contrib import admin

from posts.models import Post, PublicGroup, UserGroup, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = 'slug', 'title'
    search_fields = 'slug', 'title'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id', 'post_url', 'group',
    search_fields = 'group__title', 'id', 'post_url',
    list_filter = 'group',


@admin.register(PublicGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',
    list_filter = 'genre',


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = 'user', 'group', 'rating',
    raw_id_fields = 'user', 'group',
