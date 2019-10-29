from collections import Counter

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from voting.serializers import VoteSerializer
from voting.models import Vote


class VoteMixin(viewsets.ModelViewSet):
	serializer_class = VoteSerializer
	queryset = Vote.objects.all()
	
	def get_serializer_class(self):
		if self.action in ['retrieve', 'list', 'update', 'create']:
			return self.serializer_class
		return self.serializer_class
	
	@action(methods=['POST', 'GET'], detail=False)
	def up(self, request):
		token = request.data.get('vote_token')
		vote_params = request.data.get('vote', None)
		vote_dict = {
			"true": True,
			"false": False
		}
		
		vote = vote_dict[vote_params]
		id = request.data.get("id", None)
		model = request.data.get("model").lower()
		content_type = ContentType.objects.get(app_label=model, model=model)
		instance = content_type.get_object_for_this_type(pk=id)
		data = {'vote_token': token, 'content_type': content_type.id, 'vote': vote, 'object_id': instance.id}
		try:
			vote_instance = Vote.objects.filter(vote_token=data['vote_token'], content_type_id=data['content_type'], object_id=data['object_id'])
		except Vote.DoesNotExist:
			vote_instance = None
		if vote_instance.exists() and vote_instance.count() == 1:
			serializer = self.get_serializer(vote_instance[0], data=data, partial={'partial', False})
			serializer.is_valid(raise_exception=False)
			self.perform_update(serializer)
			response_obj = {'success': 'true', 'message': 'updated'}
		else:
			serializer = self.get_serializer(data=data)
			serializer.is_valid(raise_exception=False)
			self.perform_create(serializer)
			response_obj = {'success': 'true', 'message': 'created'}

		new_instance = instance.votes
		votes = new_instance.values_list("vote", flat=True)
		list_votes = list(votes)
		likes = list_votes.count(True)
		dislikes = list_votes.count(False)
		response_obj['likes'] = likes
		response_obj['dislikes'] = dislikes
		return Response(response_obj)
