import random

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver

from confession.managers import *
from confession.tasks import publish_confession
from core.models import ItemMetaData
from voting.models import Vote


class Confession(ItemMetaData):
	class Meta:
		db_table = 'confession'
		ordering = ['-id']
	
	class_options = (
		('primary', 'primary'),
		('success', 'success'),
		('warning', 'warning'),
	)
	
	body = models.TextField(max_length=1000, blank=True, null=False)
	css_class = models.CharField(choices=class_options, max_length=15, blank=False, null=True, default=None)
	admin_approved = models.BooleanField(default=0, blank=False, null=False)
	user_approved = models.BooleanField(default=0, blank=False, null=False)
	reported = models.BooleanField(default=0, blank=False, null=False)
	votes = GenericRelation(Vote, related_query_name="confession_votes")

	objects = ConfessionsManager()
	
	def save(self, *args, **kwargs):
		if not self.css_class:
			self.css_class = random.choices(self.class_options)[0][0]
		# if settings.DEBUG == 1:
		# 	self.admin_approved = 1
		# 	self.user_approved = 1
		super(Confession, self).save(*args, **kwargs)
	
	def __str__(self):
		return str(self.id) + ' ' + self.body[:10]


@receiver(post_save, sender=Confession)
def confession_publish(sender, instance, **kwargs):
	if instance.publish_date is not None:
		publish_confession.apply_async(args=(instance.id, ), eta=instance.publish_date)


class AllConfession(Confession):
	objects = AllConfessionsManager()

	class Meta:
		proxy = True


class ApprovedConfession(Confession):
	objects = ApprovedConfessionManager()

	class Meta:
		proxy = True


class AdminApprovedConfession(Confession):
	objects = AdminApprovedConfessionManager()

	class Meta:
		proxy = True


class ReportedConfession(Confession):
	objects = ReportedConfessionManager()

	class Meta:
		proxy = True


class ConfessionForApprove(Confession):
	objects = ConfessionForApproveManager()

	class Meta:
		proxy = True


class ConfessionUserApprovement(ItemMetaData):
	class Meta:
		db_table = "confession_user_approvement"

	confession = models.ForeignKey(Confession, on_delete=models.CASCADE)
	vote = models.IntegerField(default=1, blank=False, null=False)
	token = models.CharField(max_length=250, blank=False, null=False)
