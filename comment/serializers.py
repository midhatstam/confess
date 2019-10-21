from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.serializers import ItemMetaDataSerializer
from comment.models import Comment


class CommentSerializer(ItemMetaDataSerializer):
	reply_count = SerializerMethodField(required=False)
	likes_count = SerializerMethodField(required=False)
	dislikes_count = SerializerMethodField(required=False)
	report_count = serializers.IntegerField(required=False)

	class Meta:
		model = Comment
		fields = '__all__'
		depth = 1
		read_only_fields = ('related',)
		
	def get_reply_count(self, obj):
		if obj.item_is_parent:
			return obj.children().count()
		return 0

	def get_likes_count(self, obj):
		try:
			return len(obj.likes)
		except AttributeError:
			return 0

	def get_dislikes_count(self, obj):
		try:
			return len(obj.dislikes)
		except AttributeError:
			return 0


class CommentSerializerSingle(CommentSerializer):
	class Meta:
		model = Comment
		exclude = ('related', )
