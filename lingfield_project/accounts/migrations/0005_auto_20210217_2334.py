# Generated by Django 3.1.1 on 2021-02-17 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210216_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='items',
        ),
        migrations.AddField(
            model_name='prescription',
            name='items',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.prescriptionitem'),
            preserve_default=False,
        ),
    ]