# Generated by Django 3.1.1 on 2021-01-01 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_auto_20201221_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitallist',
            name='slug',
            field=models.SlugField(default='1'),
            preserve_default=False,
        ),
    ]
