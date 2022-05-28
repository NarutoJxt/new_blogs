# Generated by Django 3.2.6 on 2021-10-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('e', '发表'), ('d', '草稿')], default='a', max_length=1, verbose_name='文章状态'),
        ),
    ]
