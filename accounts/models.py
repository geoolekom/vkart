from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, is_active, **extra_fields):
        if 'email' in extra_fields:
            del extra_fields['email']
        user = self.model(username=username, is_staff=is_staff, is_superuser=is_superuser,
                          is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, is_active=True, **extra_fields):
        return self._create_user(username, password, False, False, is_active, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    last_name = models.CharField(verbose_name='фамилия', max_length=200)
    first_name = models.CharField(verbose_name='имя', max_length=200)

    username = models.CharField(unique=True, verbose_name='имя пользователя', max_length=150,
                                validators=[UnicodeUsernameValidator()], help_text='Обязателен. Не более 150 символов.')

    is_staff = models.BooleanField(default=False, verbose_name='персонал?')
    is_active = models.BooleanField(default=False, verbose_name='активен?')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def get_link(self):
        social_auth = self.social_auth.filter(provider='vk-oauth2').first()
        if social_auth:
            return f'https://vk.com/id{social_auth.uid}'
