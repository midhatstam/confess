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
	
	confess_body = models.TextField(max_length=1000)


class Comment(ItemMetaData):
	class Meta:
		db_table = 'comment'
	
	comment_username = models.CharField(max_length=100)
	comment_body = models.TextField(max_length=250)
	comment_parent = models.BooleanField(default=0)
	comment_related = models.ForeignKey(
		"Comment", related_name="comment_related_key", on_delete=models.CASCADE, blank=True, null=True)
