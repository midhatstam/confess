from django.db import models
from django.db.models import Prefetch, Count, Subquery

from voting.models import Vote


class ApprovedConfessionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(admin_approved=True, user_approved=True).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class AllConfessionsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().defer('css_class').prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))
