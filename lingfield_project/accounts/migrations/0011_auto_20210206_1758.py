# Generated by Django 3.1.1 on 2021-02-06 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0005_remove_medicine_user'),
        ('accounts', '0010_auto_20210206_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineitems',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medicines.medicine'),
        ),
    ]
