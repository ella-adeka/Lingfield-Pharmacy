# Generated by Django 3.1.1 on 2021-01-25 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0056_auto_20210123_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineitems',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medcineitems', to=settings.AUTH_USER_MODEL),
        ),
    ]
