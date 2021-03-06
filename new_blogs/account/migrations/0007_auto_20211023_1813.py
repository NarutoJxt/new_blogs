# Generated by Django 3.2.6 on 2021-10-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20211023_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloguser',
            old_name='head_path',
            new_name='avatar',
        ),
        migrations.AlterField(
            model_name='bloguser',
            name='gender',
            field=models.CharField(choices=[('0', '男'), ('2', '保密'), ('1', '女')], default='1', max_length=6, verbose_name='性别'),
        ),
    ]
