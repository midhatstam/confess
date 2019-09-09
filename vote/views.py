from rest_framework.decorators import list_route

from rest_framework.response import Response
from rest_framework import viewsets, filters

from django.apps import apps

from vote.models import ConfessVote, CommentVote
from vote.serializers import ConfessVoteSerializer, CommentVoteSerializer


def vote_up(self, request):
	model_params = request.POST.get('item')
	model_dict = {
		'confess': 'confess',
		'comment': 'comment'
	}
	try:
		model = apps.get_model('core', model_name=model_dict[model_params])
	except KeyError:
		return Response({'message': 'Check out "item" params'})
	
	token = request.POST.get('session_token')
	vote_params = request.POST.get('vote', None)
	vote_dict = {"true": True,
				 "false": False}
	
	vote = vote_dict[vote_params]
	id = request.POST.get("id", None)
	instance = model.objects.get(id=id)
	if model_dict[model_params] == 'confess':
		vote_instance = ConfessVote.objects.filter(vote_token=token, confess_vote_self_id=instance.id)
	else:
		vote_instance = CommentVote.objects.filter(vote_token=token, comment_vote_self_id=instance.id)
	if vote_instance.exists():
		data = {'vote_token': token, str(model_dict[model_params]) + '_vote_self': instance.id, 'vote': vote}
		serializer = self.get_serializer(vote_instance[0], data=data, partial={'partial', False})
		if serializer.is_valid(raise_exception=False):
			self.perform_update(serializer)
			return Response({'success': 'true', 'message': 'updated'})
	else:
		data = {'vote_token': token, str(model_dict[model_params]) + '_vote_self': instance.id, 'vote': vote}
		serializer = self.get_serializer(data=data)
		if serializer.is_valid(raise_exception=False):
			self.perform_create(serializer)
			return Response({'success': 'true', 'message': 'created'})
		

class ConfessVoteMixin(viewsets.ModelViewSet):
	serializer_class = ConfessVoteSerializer
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
