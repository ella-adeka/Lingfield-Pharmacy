# Generated by Django 3.1.1 on 2020-11-09 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20201109_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitallist',
            old_name='street',
            new_name='hospital_street',
        ),
    ]
