# Generated by Django 3.0.8 on 2020-10-24 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_news', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HealthNewsCategory',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
