# Generated by Django 3.2.6 on 2021-11-01 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0005_auto_20211030_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collected_time', models.DateTimeField(auto_now=True, verbose_name='收藏时间')),
                ('blog_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='collection', to=settings.AUTH_USER_MODEL, verbose_name='收藏者')),
                ('collected_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='blogs.article', verbose_name='收藏的文章')),
            ],
            options={
                'verbose_name': '收藏表',
                'ordering': ['-collected_time'],
            },
        ),
    ]
