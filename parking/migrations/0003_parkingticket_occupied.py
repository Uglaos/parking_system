# Generated by Django 2.2.7 on 2019-12-01 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_auto_20191201_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingticket',
            name='occupied',
            field=models.BooleanField(default=False),
        ),
    ]
