# Generated by Django 3.1.1 on 2021-02-15 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210212_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescriptionitem',
            name='delivery_note',
        ),
        migrations.RemoveField(
            model_name='prescriptionitem',
            name='prescription_note',
        ),
        migrations.RemoveField(
            model_name='prescriptionitem',
            name='receival',
        ),
    ]
