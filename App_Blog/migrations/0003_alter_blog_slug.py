# Generated by Django 3.2.6 on 2021-08-19 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0002_auto_20210819_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]
