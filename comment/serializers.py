from rest_framework.fields import SerializerMethodField

from core.serializers import ItemMetaDataSerializer
from comment.models import Comment


class CommentSerializer(ItemMetaDataSerializer):
	reply_count = SerializerMethodField()
	
	class Meta:
		model = Comment
		fields = '__all__'
		depth = 1
		read_only_fields = ('related',)
		
	def get_reply_count(self, obj):
		if obj.item_is_parent:
			return obj.children().count()
		return 0
