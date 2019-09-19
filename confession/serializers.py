from django.db.models import Prefetch
from rest_framework import serializers
from confession.models import Confession
from core.serializers import ItemMetaDataSerializer
from voting.models import Vote
from voting.serializers import VoteSerializer


class ConfessionSerializer(ItemMetaDataSerializer):
	num_comments = serializers.IntegerField(required=False)
	# likes = serializers.ListSerializer(child=VoteSerializer())
	# dislikes = serializers.ListSerializer(child=VoteSerializer())
	likes_count = serializers.SerializerMethodField(required=False)
	dislikes_count = serializers.SerializerMethodField(required=False)

	class Meta:
		model = Confession
		fields = '__all__'
		depth = 1

	def get_likes_count(self, obj):
		try:
			return len(obj.likes)
		except TypeError:
			return 0

	def get_dislikes_count(self, obj):
		try:
			return len(obj.dislikes)
		except TypeError:
			return 0