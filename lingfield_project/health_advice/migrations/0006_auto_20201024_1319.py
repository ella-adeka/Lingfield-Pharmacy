# Generated by Django 3.0.8 on 2020-10-24 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_advice', '0005_auto_20201024_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthadvice',
            name='categories',
            field=models.ManyToManyField(related_name='healthadvices', to='health_advice.HealthAdviceCategory', verbose_name='Category'),
        ),
    ]
