# Generated by Django 2.2.6 on 2019-10-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reported',
            field=models.BooleanField(default=0),
        ),
    ]