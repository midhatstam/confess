from rest_framework import serializers
from core.models import ItemMetaData


class ItemMetaDataSerializer(serializers.ModelSerializer):
	item_meta_data_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S.%f", read_only=True)
	
	class Meta:
		model = ItemMetaData
		exclude = ('item_meta_data_like', 'item_meta_data_dislike',)
		abstract = True
