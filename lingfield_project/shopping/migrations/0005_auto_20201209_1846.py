# Generated by Django 3.1.1 on 2020-12-09 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_delivery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': 'Delivery', 'verbose_name_plural': 'Deliveries'},
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='user',
        ),
    ]
