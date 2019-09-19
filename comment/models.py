from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import ItemMetaData
from voting.models import Vote


class Comment(ItemMetaData):
	class Meta:
		db_table = 'comment'

	username = models.CharField(max_length=100, blank=True, null=True)
	body = models.TextField()
	is_parent = models.BooleanField(default=1, blank=False, null=False)
	parent = models.ForeignKey("self", blank=True, null=True)
	related = models.ForeignKey(
		"confession.Confession", related_name="comment_related_key", on_delete=models.CASCADE, blank=True, null=True)
	removed = models.BooleanField(default=0, blank=False, null=False)
	votes = GenericRelation(Vote, related_query_name="comment_votes")

	def children(self):
		return Comment.objects.filter(parent=self)
	
	@property
	def item_is_parent(self):
		if self.parent_id is not None:
			return False
		return True
