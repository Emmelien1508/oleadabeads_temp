# Generated by Django 3.1.7 on 2021-08-13 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0004_auto_20210813_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='first',
            field=models.BooleanField(default=False),
        ),
    ]
