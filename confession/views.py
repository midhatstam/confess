from django.db.models import Count, Prefetch

from rest_framework import viewsets, status, pagination
from rest_framework.response import Response

from confession.models import ApprovedConfession
from confession.serializers import ConfessionSerializer

from comment.models import Comment
from voting.models import Vote


class CustomApiPageNumber(pagination.PageNumberPagination):
	page_size = 10


class ConfessionAPIMixin(viewsets.ModelViewSet):
	serializer_class = ConfessionSerializer
	pagination_class = CustomApiPageNumber
	lookup_field = 'id'
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AllQS(viewsets.ModelViewSet):
	queryset = ApprovedConfession.objects.all()


class PopularQS(viewsets.ModelViewSet):
	queryset = ApprovedConfession.objects.filter(item_meta_data_like__gte=200)


class BestQS(viewsets.ModelViewSet):
	comments = Comment.objects.all().values_list('related', flat=True).annotate(total=Count('id')).filter(
		total__gte=2).values_list('related', flat=True)
	queryset = ApprovedConfession.objects.filter(item_meta_data_like__gte=200, id__in=comments)


class MostLikesQS(viewsets.ModelViewSet):
	queryset = ApprovedConfession.objects.all().order_by('-item_meta_data_like')


class MostDislikesQS(viewsets.ModelViewSet):
	queryset = ApprovedConfession.objects.all().order_by('-item_meta_data_dislike')


class MostCommentsQS(viewsets.ModelViewSet):
	queryset = ApprovedConfession.objects.all().order_by('-num_comments')


class ConfessionApiView(AllQS, ConfessionAPIMixin):
	pass


class ConfessionApiPopularView(PopularQS, ConfessionAPIMixin):
	pass


class ConfessionApiBestView(BestQS, ConfessionAPIMixin):
	pass


class ConfessionApiMostLikeView(MostLikesQS, ConfessionAPIMixin):
	pass


class ConfessionApiMostDislikeView(MostDislikesQS, ConfessionAPIMixin):
	pass


class ConfessionApiMostCommentsView(MostCommentsQS, ConfessionAPIMixin):
	pass
