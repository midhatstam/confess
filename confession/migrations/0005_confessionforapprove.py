# Generated by Django 2.2.7 on 2019-11-07 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confession', '0004_confession_publish_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfessionForApprove',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('confession.confession',),
        ),
    ]