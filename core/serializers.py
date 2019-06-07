from rest_framework import serializers
from core.models import Confess, Comment, ItemMetaData


class ConfessSerializer(serializers.ModelSerializer):
	class Meta:
		model = Confess
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'


class ItemMetaDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemMetaData
		exclude = ('item_meta_data_date', )
