from django.db import models

from core.models import BaseModel


class PublicGroup(BaseModel):
    class Meta:
        verbose_name = 'паблик'
        verbose_name_plural = 'паблики'

    title = models.CharField(verbose_name='название', max_length=200)
    # screen_name = models.CharField(verbose_name='уникальное имя группы', max_length=200)
    # url = models.URLField(verbose_name='ссылка на группу')

    def __str__(self):
        return self.title


class Post(BaseModel):
    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    timestamp = models.DateTimeField(verbose_name='дата создания')

    group = models.ForeignKey('posts.PublicGroup', models.SET_NULL, blank=True, null=True)
    text = models.TextField(verbose_name='текст поста', blank=True, null=True)
    post_url = models.URLField(verbose_name='ссылка на пост')
    like_count = models.PositiveIntegerField(verbose_name='количество лайков', default=0)

    pic_url = models.URLField(verbose_name='ссылка на картинку')
    height = models.PositiveIntegerField(verbose_name='высота картинки')
    width = models.PositiveIntegerField(verbose_name='ширина картинки')

    rating = models.FloatField(verbose_name='рейтинг', default=0)

    def __str__(self):
        return f'Пост {self.id}, рейтинг {self.rating}'
