# Generated by Django 2.2.8 on 2019-12-08 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confession', '0006_confessionuserapprovement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confession',
            name='css_class',
        ),
    ]