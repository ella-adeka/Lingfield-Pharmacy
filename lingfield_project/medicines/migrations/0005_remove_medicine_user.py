# Generated by Django 3.1.1 on 2021-01-29 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0004_medicine_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='user',
        ),
    ]
