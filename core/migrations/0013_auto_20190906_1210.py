# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-09-06 12:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_commentsession_confesssession'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentsession',
            unique_together=set([('comment_session_self', 'item_session_token', 'item_is_liked')]),
        ),
        migrations.AlterUniqueTogether(
            name='confesssession',
            unique_together=set([('confess_session_self', 'item_session_token', 'item_is_liked')]),
        ),
    ]
