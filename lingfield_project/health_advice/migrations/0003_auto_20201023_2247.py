# Generated by Django 3.0.8 on 2020-10-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_advice', '0002_healthadvice_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthadvice',
            old_name='description',
            new_name='detail_description',
        ),
        migrations.AddField(
            model_name='healthadvice',
            name='list_description',
            field=models.CharField(default='a', max_length=1000),
            preserve_default=False,
        ),
    ]
