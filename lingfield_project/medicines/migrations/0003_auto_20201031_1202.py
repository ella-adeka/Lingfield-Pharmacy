# Generated by Django 3.0.8 on 2020-10-31 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0002_auto_20201030_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicines.Category', verbose_name='Category'),
        ),
    ]
