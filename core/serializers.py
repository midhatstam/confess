from rest_framework import serializers

from confession.utils import get_date
from core.models import ItemMetaData


class ItemMetaDataSerializer(serializers.ModelSerializer):
	item_meta_data_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S.%f", read_only=True)
	publish_date_format = serializers.SerializerMethodField(required=False, read_only=True)
	
	class Meta:
		model = ItemMetaData
		fields = '__all__'
		abstract = True

	@staticmethod
	def get_publish_date_format(obj):
		try:
			publish_date = obj.publish_date
		except AttributeError:
			publish_date = None
		if publish_date is not None:
			return get_date(publish_date)
