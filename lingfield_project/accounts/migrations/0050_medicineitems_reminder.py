# Generated by Django 3.1.1 on 2021-01-16 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_auto_20210116_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicineitems',
            name='reminder',
            field=models.CharField(choices=[('Never', 'Never'), ('Once', 'Once'), ('Regularly', 'Regularly')], default='None', max_length=30),
        ),
    ]
