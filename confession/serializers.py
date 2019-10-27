from rest_framework import serializers

from comment.serializers import CommentSerializer, CommentSerializerSingle
from confession.models import Confession, ApprovedConfession
from core.serializers import ItemMetaDataSerializer


class ConfessionSerializer(ItemMetaDataSerializer):
	num_comments = serializers.IntegerField(required=False, read_only=True)
	comments = CommentSerializerSingle(many=True, required=False)
	# likes = serializers.ListSerializer(child=VoteSerializer())
	# dislikes = serializers.ListSerializer(child=VoteSerializer())
	likes_count = serializers.SerializerMethodField(required=False)
	dislikes_count = serializers.SerializerMethodField(required=False)
	vote_diff = serializers.SerializerMethodField(required=False)

	class Meta:
		model = ApprovedConfession
		fields = '__all__'
		depth = 1

	@staticmethod
	def get_likes_count(obj):
		try:
			return len(obj.likes)
		except AttributeError:
			return 0

	@staticmethod
	def get_dislikes_count(obj):
		try:
			return len(obj.dislikes)
		except AttributeError:
			return 0

	@staticmethod
	def get_vote_diff(obj):
		try:
			diff = len(obj.likes) - len(obj.dislikes)
			return diff
		except AttributeError:
			return 0
