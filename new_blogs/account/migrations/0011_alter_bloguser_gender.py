# Generated by Django 3.2.6 on 2021-10-30 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20211024_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='gender',
            field=models.CharField(choices=[('2', '保密'), ('1', '女'), ('0', '男')], default='1', max_length=6, verbose_name='性别'),
        ),
    ]
