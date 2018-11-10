# Generated by Django 2.1.2 on 2018-11-10 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_publicgroup_screen_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.PublicGroup', verbose_name='группа')),
            ],
            options={
                'verbose_name': 'группа постов',
                'verbose_name_plural': 'группы постов',
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.PublicGroup', verbose_name='группа'),
        ),
        migrations.AddField(
            model_name='postgroup',
            name='posts',
            field=models.ManyToManyField(to='posts.Post', verbose_name='посты'),
        ),
        migrations.AddField(
            model_name='postgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
