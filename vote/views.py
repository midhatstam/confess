from django.apps import apps
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route
from rest_framework.response import Response

from comment import serializers
from confession import serializers
from vote.models import ConfessionVote, CommentVote
from vote.serializers import ConfessionVoteSerializer, CommentVoteSerializer


def vote_up(self, request):
	model_params = request.POST.get('item').lower()
	model_dict = {
		'confession': 'confession',
		'comment': 'comment'
	}
	try:
		model = apps.get_model(model_dict[model_params], model_name=model_dict[model_params])
	except KeyError:
		return Response({'message': 'Check out "item" params'})
	
	token = request.COOKIES.get('session_token')
	vote_params = request.POST.get('vote', None)
	vote_dict = {
		"true": True,
		"false": False
	}
	
	vote = vote_dict[vote_params]
	id = request.POST.get("id", None)
	instance = model.objects.get(id=id)
	if model_dict[model_params] == 'confession':
		vote_instance = ConfessionVote.objects.filter(vote_token=token, confession_vote_self_id=instance.id)
	else:
		vote_instance = CommentVote.objects.filter(vote_token=token, comment_vote_self_id=instance.id)
	
	data = {'vote_token': token, str(model_dict[model_params]) + '_vote_self': instance.id, 'vote': vote}
	if vote_instance.exists():
		serializer = self.get_serializer(vote_instance[0], data=data, partial={'partial', False})
		serializer.is_valid(raise_exception=False)
		self.perform_update(serializer)
		response_obj = {'success': 'true', 'message': 'updated'}
	else:
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=False)
		self.perform_create(serializer)
		response_obj = {'success': 'true', 'message': 'created'}
	
	new_instance = model.objects.get(id=id)
	instance_serializer_class = getattr(serializers, model_dict[model_params].capitalize() + 'Serializer')
	instance_serializer = instance_serializer_class(new_instance, many=False).data
	response_obj['item'] = instance_serializer
	return Response(response_obj)


class ConfessionVoteMixin(viewsets.ModelViewSet):
	serializer_class = ConfessionVoteSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter)
	
	def get_serializer_class(self):
		if self.action in ['retrieve', 'list', 'update', 'create']:
			return self.serializer_class
		return self.serializer_class
	
	@list_route(methods=['POST', 'GET'])
	def up(self, request):
		return vote_up(self, request)


class CommentVoteMixin(viewsets.ModelViewSet):
	serializer_class = CommentVoteSerializer
	
	def get_serializer_class(self):
		if self.action in ['retrieve', 'list', 'update', 'create']:
			return self.serializer_class
		return self.serializer_class
	
	@list_route(methods=['POST', 'GET'])
	def up(self, request):
		return vote_up(self, request)
