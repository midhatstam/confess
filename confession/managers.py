from random import randint

from django.db import models
from django.db.models import Prefetch, Count

from voting.models import Vote


class ConfessionsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().defer('css_class').prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class AllConfessionsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(reported=False).defer('css_class').prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class ApprovedConfessionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(admin_approved=True, user_approved=True, reported=False).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class AdminApprovedConfessionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(admin_approved=True, reported=False).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class ReportedConfessionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(reported=True).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))


class ConfessionForApproveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(admin_approved=True, user_approved=False, reported=False).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=1), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=1), to_attr='dislikes')
        ).annotate(num_comments=Count('comments'))

    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
