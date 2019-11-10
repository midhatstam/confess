from rest_framework import serializers

from comment.serializers import CommentSerializer, CommentSerializerSingle
from confession.models import Confession, ApprovedConfession, ConfessionUserApprovement
from core.serializers import ItemMetaDataSerializer


class ConfessionSerializer(ItemMetaDataSerializer):
	num_comments = serializers.IntegerField(required=False, read_only=True)
	comments = CommentSerializerSingle(many=True, required=False)
	# likes = serializers.ListSerializer(child=VoteSerializer())
	# dislikes = serializers.ListSerializer(child=VoteSerializer())
	likes_count = serializers.SerializerMethodField(required=False, read_only=True)
	dislikes_count = serializers.SerializerMethodField(required=False, read_only=True)
	vote_diff = serializers.SerializerMethodField(required=False, read_only=True)

	class Meta:
		model = Confession
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


class ConfessionUserApprovementSerializer(ItemMetaDataSerializer):
	class Meta:
		model = ConfessionUserApprovement
		fields = '__all__'
		depth = 1
		read_only_fields = ("related", )
