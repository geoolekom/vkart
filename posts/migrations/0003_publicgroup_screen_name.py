# Generated by Django 2.1.2 on 2018-11-10 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20181110_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicgroup',
            name='screen_name',
            field=models.CharField(default='', max_length=200, verbose_name='уникальное имя группы'),
            preserve_default=False,
        ),
    ]
