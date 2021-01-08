# Generated by Django 3.1.1 on 2020-11-15 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0030_auto_20201115_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dependent', to=settings.AUTH_USER_MODEL),
        ),
    ]
