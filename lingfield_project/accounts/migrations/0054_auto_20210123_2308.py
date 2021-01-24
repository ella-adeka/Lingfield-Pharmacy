# Generated by Django 3.1.1 on 2021-01-23 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0053_auto_20210123_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicineitems',
            name='user',
        ),
        migrations.AddField(
            model_name='medicineitems',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medicineitems', to=settings.AUTH_USER_MODEL),
        ),
    ]
