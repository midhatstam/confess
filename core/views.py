from __future__ import absolute_import

import uuid

from collections import OrderedDict

from django.db.models import Count

from rest_framework.response import Response
from rest_framework import viewsets, pagination, status
from rest_framework.renderers import TemplateHTMLRenderer

from core.models import Confess, Comment
from core.serializers import ConfessSerializer


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
