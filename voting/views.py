from collections import Counter

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import list_route
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
	
	@list_route(methods=['POST', 'GET'])
	def up(self, request):
		token = request.POST.get('vote_token')
		vote_params = request.POST.get('vote', None)
		vote_dict = {
			"true": True,
			"false": False
		}
		
		vote = vote_dict[vote_params]
		id = request.POST.get("id", None)
		model = request.POST.get("model").lower()
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
		
		model_dict = {
			'confession': 'confession',
			'comment': 'comment'
		}
		try:
			model_obj = apps.get_model(model_dict[model], model_name=model_dict[model])
		except KeyError:
			return Response({'message': 'Check out "item" params'})
		
		new_instance = instance.votes
		votes = new_instance.values_list("vote", flat=True)
		print(votes)
		# print(votes)
		likes = new_instance.filter(vote=1).count()
		dislikes = new_instance.filter(vote=0).count()
		response_obj['likes'] = likes
		response_obj['dislikes'] = dislikes
		# response_obj['votes'] = votes
		# response_obj['votes_likes'] = votes
		return Response(response_obj)
