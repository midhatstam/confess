from django.contrib.contenttypes.models import ContentType
from django.db import models, DataError

from comment.models import Comment
from confession.models import Confession


class ItemVoteData(models.Model):
	class Meta:
		db_table = "item_vote_data"
		abstract = True
	
	vote_token = models.CharField(max_length=250, blank=False, null=False)
	vote = models.BooleanField(default=1, blank=False, null=False)


class ConfessionVote(ItemVoteData):
	class Meta:
		db_table = 'confession_vote'
		unique_together = [
			'confession_vote_self', 'vote_token'
		]
	
	confession_vote_self = models.ForeignKey(
		'confession.Confession', related_name='confession_vote_self_key', on_delete=models.CASCADE, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		try:
			confession = Confession.objects.get(id=self.confession_vote_self_id)
		except Confession.DoesNotExist:
			confession = None
		
		if confession is not None:
			if self.pk is None:
				if self.vote == True:
					try:
						confession.item_meta_data_like += 1
					except TypeError:
						confession.item_meta_data_like = 1
				else:
					try:
						confession.item_meta_data_dislike += 1
					except TypeError:
						confession.item_meta_data_dislike = 1
			else:
				current_confession_session = ConfessionVote.objects.get(id=self.pk)
				if current_confession_session.vote == self.vote:
					pass
				else:
					if self.vote == True:
						try:
							confession.item_meta_data_like += 1
						except DataError:
							confession.item_meta_data_like = 1
						try:
							confession.item_meta_data_dislike += -1
						except DataError:
							confession.item_meta_data_dislike = 0
					else:
						try:
							confession.item_meta_data_dislike += 1
						except DataError:
							confession.item_meta_data_dislike = 1
						try:
							confession.item_meta_data_like += -1
						except DataError:
							confession.item_meta_data_like = 0
			confession.save()
			super(ConfessionVote, self).save(*args, **kwargs)
		else:
			print('confession not found')


class CommentVote(ItemVoteData):
	class Meta:
		db_table = 'comment_vote'
		unique_together = [
			'comment_vote_self', 'vote_token'
		]
	
	comment_vote_self = models.ForeignKey(
		'comment.Comment', related_name='comment_vote_self_key', on_delete=models.CASCADE, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		try:
			comment = Comment.objects.get(id=self.comment_vote_self_id)
		except Comment.DoesNotExist:
			comment = None
		
		if comment is not None:
			if self.pk is None:
				if self.vote == True:
					comment.item_meta_data_like += 1
				else:
					comment.item_meta_data_dislike += 1
			else:
				current_comment_session = CommentVote.objects.get(id=self.pk)
				if current_comment_session.vote == self.vote:
					pass
				else:
					if self.vote == True:
						comment.item_meta_data_like += 1
						comment.item_meta_data_dislike += -1
					else:
						comment.item_meta_data_dislike += 1
						comment.item_meta_data_like += -1
			comment.save()
			super(CommentVote, self).save(*args, **kwargs)
		else:
			print('confession not found')
