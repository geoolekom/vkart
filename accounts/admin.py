from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = '-date_joined', 'username',
    readonly_fields = 'date_joined', 'last_login'
    list_display = 'username', 'last_name', 'first_name', 'date_joined', 'last_login',
    list_filter = 'is_active', 'is_staff', 'is_superuser',

    search_fields = 'username',
    filter_horizontal = 'groups', 'user_permissions',

    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        ('Даты', {'fields': ('date_joined', 'last_login', )}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2'),
            'classes': ('wide',),
        }),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
    )
