from rest_framework import serializers
from core.models import Confess, Comment, ItemMetaData


class ItemMetaDataSerializer(serializers.ModelSerializer):
	item_meta_data_date = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)
	
	class Meta:
		model = ItemMetaData
		exclude = ('item_meta_data_like', 'item_meta_data_dislike',)
		abstract = True


class ConfessSerializer(ItemMetaDataSerializer):
	class Meta:
		model = Confess
		fields = '__all__'


class CommentSerializer(ItemMetaDataSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
