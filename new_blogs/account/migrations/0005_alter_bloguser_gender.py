# Generated by Django 3.2.6 on 2021-10-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_bloguser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='gender',
            field=models.CharField(choices=[('1', '女'), ('0', '男'), ('2', '保密')], default='1', max_length=6, verbose_name='性别'),
        ),
    ]
