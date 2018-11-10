from django.conf import settings
from django.db import models

from core.models import BaseModel


class PublicGroup(BaseModel):
    class Meta:
        verbose_name = 'паблик'
        verbose_name_plural = 'паблики'

    title = models.CharField(verbose_name='название', max_length=200)
    screen_name = models.CharField(verbose_name='уникальное имя группы', max_length=200)

    def __str__(self):
        return f'{self.screen_name}: {self.title}'


class Post(models.Model):
    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    timestamp = models.DateTimeField(verbose_name='дата создания')

    group = models.ForeignKey('posts.PublicGroup', models.SET_NULL, blank=True, null=True, verbose_name='группа')
    text = models.TextField(verbose_name='текст поста', blank=True, null=True)
    post_url = models.URLField(verbose_name='ссылка на пост')
    like_count = models.PositiveIntegerField(verbose_name='количество лайков', default=0)

    pic_url = models.URLField(verbose_name='ссылка на картинку')
    height = models.PositiveIntegerField(verbose_name='высота картинки')
    width = models.PositiveIntegerField(verbose_name='ширина картинки')

    rating = models.FloatField(verbose_name='рейтинг', default=0)
    vk_id = models.BigIntegerField(verbose_name='ВК id')

    def __str__(self):
        return f'Пост {self.id} из {self.group}, рейтинг {self.rating}'


class UserGroup(models.Model):
    class Meta:
        verbose_name = 'пользователь в группе'
        verbose_name_plural = 'пользователи в группе'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name='пользователь')
    group = models.ForeignKey('posts.PublicGroup', models.CASCADE, verbose_name='группа')
    rating = models.FloatField(verbose_name='рейтинг', default=0)

    def __str__(self):
        return f'{self.user} в {self.group.title}'
