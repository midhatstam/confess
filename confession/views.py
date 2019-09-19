from django.db.models import Count

from rest_framework import viewsets, status, pagination
from rest_framework.response import Response

from confession.models import Confession
from confession.serializers import ConfessionSerializer

from comment.models import Comment


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
	queryset = Confession.objects.filter(admin_approved=True).annotate(
		num_comments=Count('comment_related_key'))


class PopularQS(viewsets.ModelViewSet):
	queryset = Confession.objects.filter(admin_approved=True, item_meta_data_like__gte=200).annotate(
		num_comments=Count('comment_related_key'))


class BestQS(viewsets.ModelViewSet):
	comments = Comment.objects.all().values_list('related', flat=True).annotate(total=Count('id')).filter(
		total__gte=2).values_list('related', flat=True)
	queryset = Confession.objects.filter(admin_approved=True, item_meta_data_like__gte=200,
									  id__in=comments).annotate(num_comments=Count('comment_related_key'))


class MostLikesQS(viewsets.ModelViewSet):
	queryset = Confession.objects.filter(admin_approved=True).order_by('-item_meta_data_like').annotate(
		num_comments=Count('comment_related_key'))


class MostDislikesQS(viewsets.ModelViewSet):
	queryset = Confession.objects.filter(admin_approved=True).order_by('-item_meta_data_dislike').annotate(
		num_comments=Count('comment_related_key'))


class MostCommentsQS(viewsets.ModelViewSet):
	queryset = Confession.objects.filter(admin_approved=True).annotate(
		num_comments=Count('comment_related_key')).order_by('-num_comments')


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
