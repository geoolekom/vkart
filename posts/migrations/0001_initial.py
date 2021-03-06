# Generated by Django 2.1.2 on 2018-11-09 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False, verbose_name='ВК id')),
                ('timestamp', models.DateTimeField(verbose_name='дата создания')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст поста')),
                ('post_url', models.URLField(verbose_name='ссылка на пост')),
                ('like_count', models.PositiveIntegerField(default=0, verbose_name='количество лайков')),
                ('pic_url', models.URLField(verbose_name='ссылка на картинку')),
                ('height', models.PositiveIntegerField(verbose_name='высота картинки')),
                ('width', models.PositiveIntegerField(verbose_name='ширина картинки')),
                ('rating', models.PositiveIntegerField(default=0, verbose_name='рейтинг')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
        migrations.CreateModel(
            name='PublicGroup',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False, verbose_name='ВК id')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
            ],
            options={
                'verbose_name': 'паблик',
                'verbose_name_plural': 'паблики',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.PublicGroup'),
        ),
    ]
