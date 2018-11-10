from django.contrib import admin

from posts.models import Post, PublicGroup, PostGroup, UserGroup


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id', 'post_url', 'group'
    search_fields = 'group__title', 'id', 'post_url',


@admin.register(PublicGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',


@admin.register(PostGroup)
class PostGroupAdmin(admin.ModelAdmin):
    list_display = 'user', 'group'
    raw_id_fields = 'user', 'group', 'posts'


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = 'user', 'group', 'rating',
    raw_id_fields = 'user', 'group',
