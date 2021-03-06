# Generated by Django 3.2.6 on 2021-11-04 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
        ('compliment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplimentForComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('praise_time', models.DateTimeField(auto_now=True, verbose_name='点赞时间')),
                ('blog_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='点赞者')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.comment', verbose_name='被点赞的文章')),
            ],
            options={
                'verbose_name': 'compliment_for_comment',
            },
        ),
    ]
