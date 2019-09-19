from django.db import models


class ItemMetaData(models.Model):
	class Meta:
		db_table = "item_meta_data"
		abstract = True
		unique_together = [
			'item_meta_data_like', 'item_meta_data_dislike', 'item_meta_data_date']
	
	item_meta_data_like = models.PositiveIntegerField(default=0, blank=False, null=False)
	item_meta_data_dislike = models.PositiveIntegerField(default=0, blank=False, null=False)
	item_meta_data_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
