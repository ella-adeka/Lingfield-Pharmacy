# Generated by Django 3.1.1 on 2020-11-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_hospitallist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitallist',
            name='distirct',
        ),
        migrations.AddField(
            model_name='hospitallist',
            name='district',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
