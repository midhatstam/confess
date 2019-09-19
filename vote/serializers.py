from rest_framework import serializers
from vote.models import ItemVoteData, ConfessionVote, CommentVote


class ItemVoteDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemVoteData
		fields = '__all__'


class ConfessionVoteSerializer(ItemVoteDataSerializer):
	class Meta:
		model = ConfessionVote
		fields = '__all__'


class CommentVoteSerializer(ItemVoteDataSerializer):
	class Meta:
		model = CommentVote
		fields = '__all__'
