from django.db import models


# Create your models here.


class Confess(models.Model):
	class Meta:
		db_table = 'confess'
	
	confess_body = models.TextField(max_length=1000)


class Comment(models.Model):
	class Meta:
		db_table = 'comment'
	
	comment_username = models.CharField(max_length=100)
	comment_body = models.TextField(max_length=250)
	comment_parent = models.BooleanField(default=0)
	comment_related = models.ForeignKey(
		"Comment", related_name="comment_related_key", on_delete=models.CASCADE, blank=True, null=True)


ITEM_CHOICES = (
	('CONF', 'Confess'),
	('COMM', 'Comment'),
)


class ItemMetaData(models.Model):
	class Meta:
		db_table = "item_meta_data"
		unique_together = [
			'item_meta_data_type', 'item_meta_data_confess', 'item_meta_data_comment', 'item_meta_data_like',
			'item_meta_data_dislike', 'item_meta_data_date']
	
	item_meta_data_type = models.CharField(max_length=4, choices=ITEM_CHOICES, blank=False, null=False)
	item_meta_data_confess = models.ForeignKey(
		"Confess", related_name="item_meta_data_confess_key", on_delete=models.CASCADE, blank=True, null=True)
	item_meta_data_comment = models.ForeignKey(
		"Comment", related_name="item_meta_data_comment_key", on_delete=models.CASCADE, blank=True, null=True)
	item_meta_data_like = models.IntegerField()
	item_meta_data_dislike = models.IntegerField()
	item_meta_data_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
