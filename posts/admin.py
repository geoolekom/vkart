from django.contrib import admin

from posts.models import Post, PublicGroup, PostGroup


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id', 'post_url', 'group'
    search_fields = 'group__title', 'id', 'post_url',


@admin.register(PublicGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',


@admin.register(PostGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = 'user', 'group'
    raw_id_fields = 'user', 'group'
