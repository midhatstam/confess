# Generated by Django 2.2.8 on 2019-12-07 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0002_insertdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
