from django.db.models import Count

from rest_framework import viewsets, status, pagination, generics
from rest_framework.response import Response

from confession.models import ApprovedConfession, ConfessionForApprove, ConfessionUserApprovement
from confession.serializers import ConfessionSerializer, ConfessionUserApprovementSerializer

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
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AllQS(viewsets.ModelViewSet):
    queryset = ApprovedConfession.objects.all()


class PopularQS(viewsets.ModelViewSet):
    queryset = ApprovedConfession.objects.filter(votes__gte=200)


class BestQS(viewsets.ModelViewSet):
    comments = Comment.objects.all().values_list(
        'related', flat=True
    ).annotate(total=Count('id')).filter(
        total__gte=2).values_list('related', flat=True)
    queryset = ApprovedConfession.objects.filter(
        votes__gte=200, id__in=comments
    )


class MostLikesQS(generics.ListAPIView):
    queryset = ApprovedConfession.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        serializer_data = sorted(
            serializer.data, key=lambda k: k['vote_diff'], reverse=True)
        return Response(serializer_data)


class MostDislikesQS(viewsets.ModelViewSet):
    queryset = ApprovedConfession.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        serializer_data = sorted(
            serializer.data, key=lambda k: k['vote_diff'], reverse=False)
        return Response(serializer_data)


class MostCommentsQS(viewsets.ModelViewSet):
    queryset = ApprovedConfession.objects.all().order_by('-num_comments')


class ConfessionForApproveView(viewsets.ModelViewSet):
    serializer_class = ConfessionSerializer

    def get_queryset(self):
        try:
            return ConfessionForApprove.objects.random()
        except TypeError:
            return []

    def retrieve(self, request, *args, **kwargs):
        token = request.COOKIES.get('session_token')
        approved_instances_id = ConfessionUserApprovement.objects.filter(token=token).values_list('id')
        instance = self.get_queryset().exclude(approved_instances_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConfessionUserApprovementView(viewsets.ModelViewSet):
    serializer_class = ConfessionUserApprovementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


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


class ConfessionApiForApprove(ConfessionForApproveView, ConfessionAPIMixin):
    pass
