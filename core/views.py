from __future__ import absolute_import

import uuid

from collections import OrderedDict

from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.renderers import TemplateHTMLRenderer

from confession.views import ConfessionAPIMixin, AllQS, PopularQS, BestQS, MostLikesQS, MostDislikesQS, MostCommentsQS


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


class ConfessionHTMLMixin(ConfessionAPIMixin):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'main/index.html'
	pagination_class = CustomPageNumber
	
	def finalize_response(self, request, response, *args, **kwargs):
		token = uuid.uuid4()
		response_obj = super(ConfessionHTMLMixin, self).finalize_response(
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


class ConfessionView(AllQS, ConfessionHTMLMixin):
	pass


class ConfessionPopularView(PopularQS, ConfessionHTMLMixin):
	pass


class ConfessionBestView(BestQS, ConfessionHTMLMixin):
	pass


class ConfessionMostLikeView(MostLikesQS, ConfessionHTMLMixin):
	pass


class ConfessionMostDislikeView(MostDislikesQS, ConfessionHTMLMixin):
	pass


class ConfessionMostCommentsView(MostCommentsQS, ConfessionHTMLMixin):
	pass
