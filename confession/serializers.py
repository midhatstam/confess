from rest_framework import serializers
from confession.models import Confession
from core.serializers import ItemMetaDataSerializer


class ConfessionSerializer(ItemMetaDataSerializer):
	num_comments = serializers.IntegerField(required=False)
	
	class Meta:
		model = Confession
		fields = '__all__'
