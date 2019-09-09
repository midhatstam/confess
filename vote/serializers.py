from rest_framework import serializers
from vote.models import ItemVoteData, ConfessVote, CommentVote


class ItemVoteDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemVoteData
		fields = '__all__'


class ConfessVoteSerializer(ItemVoteDataSerializer):
	class Meta:
		model = ConfessVote
		fields = '__all__'


class CommentVoteSerializer(ItemVoteDataSerializer):
	class Meta:
		model = CommentVote
		fields = '__all__'
