# Generated by Django 3.1.1 on 2021-02-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0009_remove_shop_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='directions',
            field=models.TextField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name='shop',
            name='first_description',
            field=models.TextField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name='shop',
            name='ingredients',
            field=models.TextField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name='shop',
            name='second_description',
            field=models.TextField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name='shop',
            name='warnings',
            field=models.TextField(max_length=1000000),
        ),
    ]
