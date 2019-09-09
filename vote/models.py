from django.db import models

from core.models import Confess, Comment


class ItemVoteData(models.Model):
	class Meta:
		db_table = "item_vote_data"
		abstract = True
	
	vote_token = models.CharField(max_length=250, blank=False, null=False)
	vote = models.BooleanField(default=1, blank=False, null=False)


class ConfessVote(ItemVoteData):
	class Meta:
		db_table = 'confess_vote'
		unique_together = [
			'confess_vote_self', 'vote_token'
		]
	
	confess_vote_self = models.ForeignKey(
		'core.Confess', related_name='confess_vote_self_key', on_delete=models.CASCADE, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		try:
			confess = Confess.objects.get(id=self.confess_vote_self_id)
		except:
			confess = None
		
		if confess is not None:
			if self.pk is None:
				if self.vote == True:
					confess.item_meta_data_like += 1
				else:
					confess.item_meta_data_dislike += 1
			else:
				current_confess_session = ConfessVote.objects.get(id=self.pk)
				if current_confess_session.vote == self.vote:
					pass
				else:
					if self.vote == True:
						confess.item_meta_data_like += 1
						confess.item_meta_data_dislike += -1
					else:
						confess.item_meta_data_dislike += 1
						confess.item_meta_data_like += -1
			try:
				confess.save()
			except:
				print('cant save')
		else:
			print('confess not found')
		super(ConfessVote, self).save(*args, **kwargs)


class CommentVote(ItemVoteData):
	class Meta:
		db_table = 'comment_vote'
		unique_together = [
			'comment_vote_self', 'vote_token'
		]
	
	comment_vote_self = models.ForeignKey(
		'core.Comment', related_name='comment_vote_self_key', on_delete=models.CASCADE, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		try:
			comment = Comment.objects.get(id=self.comment_vote_self_id)
		except:
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
			try:
				comment.save()
			except:
				print('cant save')
		else:
			print('confess not found')
		super(CommentVote, self).save(*args, **kwargs)
