# Generated by Django 3.1.1 on 2021-02-06 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0005_remove_medicine_user'),
        ('accounts', '0012_auto_20210206_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineitems',
            name='item',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='medicines.medicine'),
        ),
    ]
