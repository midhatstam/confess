import random

from django.db import models


# Create your models here.


class ItemMetaData(models.Model):
	class Meta:
		db_table = "item_meta_data"
		abstract = True
		unique_together = [
			'item_meta_data_like', 'item_meta_data_dislike', 'item_meta_data_date']
	
	item_meta_data_like = models.IntegerField(blank=True, null=True)
	item_meta_data_dislike = models.IntegerField(blank=True, null=True)
	item_meta_data_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)


class Confess(ItemMetaData):
	class Meta:
		db_table = 'confess'
		ordering = ['-id']
	
	class_options = (
		('primary', 'primary'),
		('success', 'success'),
		('warning', 'warning'),
	)
	
	confess_body = models.TextField(max_length=1000, blank=True, null=False)
	confess_class = models.CharField(choices=class_options, max_length=15, blank=False, null=True, default=None)
	confess_admin_approved = models.BooleanField(default=0, blank=False, null=False)
	confess_user_approved = models.BooleanField(default=0, blank=False, null=False)
	
	def save(self, *args, **kwargs):
		if not self.confess_class:
			self.confess_class = random.choices(self.class_options)[0][0]
		super(Confess, self).save(*args, **kwargs)
		
	def __str__(self):
		return str(self.id) + ' ' + self.confess_body[:10]
	

class Comment(ItemMetaData):
	class Meta:
		db_table = 'comment'
	
	comment_username = models.CharField(max_length=100)
	comment_body = models.TextField(max_length=250)
	comment_parent = models.BooleanField(default=0)
	comment_related = models.ForeignKey(
		"Confess", related_name="comment_related_key", on_delete=models.CASCADE, blank=True, null=True)
	comment_removed = models.BooleanField(default=0, blank=False, null=False)
