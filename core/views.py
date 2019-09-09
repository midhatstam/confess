from __future__ import absolute_import

import uuid

from collections import OrderedDict

from django.http import QueryDict

from django.db.models import Count, Case, When, Prefetch, Value, IntegerField, BooleanField

from rest_framework.response import Response
from rest_framework import viewsets, pagination, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics

from core.models import Confess, Comment, ItemMetaData, ItemSessionData, ConfessSession, CommentSession
from core.serializers import ConfessSerializer, CommentSerializer, ItemMetaDataSerializer, ItemSessionDataSerializer, \
	ConfessSessionSerializer, CommentSessionSerializer


class CustomPageNumber(pagination.PageNumberPagination):
	page_size = 10
	
	def get_paginated_response(self, data):
		page_range = self.page.paginator.page_range
		index = self.page.number - 1
		max_index = len(page_range)
		start_index = index - 2 if index >= 2 else 0
		end_index = index + 5 if index <= max_index - 5 else max_index
		page_range = list(page_range)[start_index:end_index]
		
		return Response(OrderedDict([
			('lastPage', self.page.paginator.count),
			('countItemsOnPage', self.page_size),
			('current', self.page.number),
			('next', self.page.next_page_number),
			('previous', self.page.previous_page_number),
			('results', data),
			('has_next', self.page.has_next),
			('has_previous', self.page.has_previous),
			('page_range', page_range),
			('number', self.page.number),
		]))


class CustomApiPageNumber(pagination.PageNumberPagination):
	page_size = 10


class ConfessAPIMixin(viewsets.ModelViewSet):
	serializer_class = ConfessSerializer
	pagination_class = CustomApiPageNumber
	lookup_field = 'id'
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
	
	def patch(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', True)
		instance = self.get_object()
		data = {}
		if request.data.get('like') == "1":
			if request.data.get('dislike') == "0":
				if instance.item_meta_data_like is not None:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_like'] = instance.item_meta_data_like + 1
						if instance.item_meta_data_dislike is not None:
							data['item_meta_data_dislike'] = instance.item_meta_data_dislike - 1
				else:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_like'] = 1
						if instance.item_meta_data_dislike is not None:
							data['item_meta_data_dislike'] = instance.item_meta_data_dislike - 1
			else:
				if instance.item_meta_data_like is not None:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_like'] = instance.item_meta_data_like + 1
				else:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_like'] = 1
		elif request.data.get('dislike') == "1":
			if request.data.get('like') == "0":
				if instance.item_meta_data_dislike is not None:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_dislike'] = instance.item_meta_data_dislike + 1
						if instance.item_meta_data_like is not None:
							data['item_meta_data_like'] = instance.item_meta_data_like - 1
				else:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_dislike'] = 1
						if instance.item_meta_data_like is not None:
							data['item_meta_data_like'] = instance.item_meta_data_like - 1
			else:
				if instance.item_meta_data_dislike is not None:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_dislike'] = instance.item_meta_data_dislike + 1
				else:
					if ConfessSessionMixin.as_view({'put': 'create'})(request._request).status_code == 400:
						return Response(status=status.HTTP_200_OK)
					else:
						data['item_meta_data_dislike'] = 1
		qdata = QueryDict('', mutable=True)
		qdata.update(data)
		serializer = self.get_serializer(instance, data=qdata, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfessSessionMixin(viewsets.ModelViewSet):
	serializer_class = ConfessSessionSerializer
	lookup_field = 'id'
	
	def create(self, request, *args, **kwargs):
		data = {}
		data['item_session_token'] = request.COOKIES.get('session_token')
		data['confess_session_self'] = int(request.POST.get('id'))
		try:
			like = request.POST.get('like')
		except:
			like = None
		
		try:
			dislike = request.POST.get('dislike')
		except:
			dislike = None
		
		if like is not None:
			if dislike is not None:
				if like == "0":
					data['item_is_liked'] = 0
				else:
					data['item_is_liked'] = 1
			else:
				data['item_is_liked'] = 1
		else:
			data['item_is_liked'] = 0
		
		qdata = QueryDict('', mutable=True)
		qdata.update(data)
		try:
			current_session = ConfessSession.objects.get(
				item_session_token=request.COOKIES.get('session_token'),
				confess_session_self_id=int(request.POST.get('id')),
			)
		except:
			current_session = None
		
		if current_session is not None:
			if int(current_session.item_is_liked) == int(data['item_is_liked']):
				return Response(status=status.HTTP_400_BAD_REQUEST)
			else:
				serializer = ConfessSessionSerializer(current_session, data=qdata)
				serializer.is_valid(raise_exception=True)
				self.perform_update(serializer)
		else:
			serializer = self.get_serializer(data=qdata)
			# serializer = ConfessSessionSerializer(data=qdata)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, headers=headers)


class ConfessHTMLMixin(ConfessAPIMixin):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'main/index.html'
	pagination_class = CustomPageNumber
	
	def finalize_response(self, request, response, *args, **kwargs):
		token = uuid.uuid4()
		response_obj = super(ConfessHTMLMixin, self).finalize_response(
			request, response, *args, **kwargs)
		
		try:
			cookie = request.COOKIES.get('session_token')
		except:
			cookie = None
		if cookie is None:
			response_obj.set_cookie(
				'session_token', token
			)
		else:
			pass
		return response


class AllQS(viewsets.ModelViewSet):
	queryset = Confess.objects.filter(confess_admin_approved=True).annotate(
		num_comments=Count('comment_related_key'))


class PopularQS(viewsets.ModelViewSet):
	queryset = Confess.objects.filter(confess_admin_approved=True, item_meta_data_like__gte=200).annotate(
		num_comments=Count('comment_related_key'))


class BestQS(viewsets.ModelViewSet):
	comments = Comment.objects.all().values_list('comment_related', flat=True).annotate(total=Count('id')).filter(
		total__gte=2).values_list('comment_related', flat=True)
	queryset = Confess.objects.filter(confess_admin_approved=True, item_meta_data_like__gte=200,
									  id__in=comments).annotate(num_comments=Count('comment_related_key'))


class MostLikesQS(viewsets.ModelViewSet):
	queryset = Confess.objects.filter(confess_admin_approved=True).order_by('-item_meta_data_like').annotate(
		num_comments=Count('comment_related_key'))


class MostDislikesQS(viewsets.ModelViewSet):
	queryset = Confess.objects.filter(confess_admin_approved=True).order_by('-item_meta_data_dislike').annotate(
		num_comments=Count('comment_related_key'))


class MostCommentsQS(viewsets.ModelViewSet):
	queryset = Confess.objects.filter(confess_admin_approved=True).annotate(
		num_comments=Count('comment_related_key')).order_by('-num_comments')


class ConfessView(AllQS, ConfessHTMLMixin):
	pass


class ConfessApiView(AllQS, ConfessAPIMixin):
	pass


class ConfessPopularView(PopularQS, ConfessHTMLMixin):
	pass


class ConfessApiPopularView(PopularQS, ConfessAPIMixin):
	pass


class ConfessBestView(BestQS, ConfessHTMLMixin):
	pass


class ConfessApiBestView(BestQS, ConfessAPIMixin):
	pass


class ConfessMostLikeView(MostLikesQS, ConfessHTMLMixin):
	pass


class ConfessApiMostLikeView(MostLikesQS, ConfessAPIMixin):
	pass


class ConfessMostDislikeView(MostDislikesQS, ConfessHTMLMixin):
	pass


class ConfessApiMostDislikeView(MostDislikesQS, ConfessAPIMixin):
	pass


class ConfessMostCommentsView(MostCommentsQS, ConfessHTMLMixin):
	pass


class ConfessApiMostCommentsView(MostCommentsQS, ConfessAPIMixin):
	pass
