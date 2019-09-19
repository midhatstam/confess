from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from six import text_type


VOTES = (
	(+1, '+1'),
	(-1, '-1'),
)


class Vote(models.Model):
	vote_token = models.CharField(max_length=250, blank=False, null=False)
	# vote = models.SmallIntegerField(choices=VOTES, blank=False, null=False)
	vote = models.BooleanField(default=1, blank=False, null=False)
	
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()
	created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, db_index=True, null=True)
	
	class Meta:
		db_table = 'vote'
		unique_together = [
			'vote_token', 'content_type'
		]
	
	def __str__(self):
		return text_type('{} from {} on {}').format(self.vote, self.vote_token, self.content_object)
