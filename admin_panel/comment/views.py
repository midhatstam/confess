from rest_framework import generics

from comment.models import Comment
from comment.serializers import CommentSerializer
from core.views import CustomPageNumber


class AdminApiPageNumber(CustomPageNumber):
    page_size = 25


class CommentMixin(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = AdminApiPageNumber
    lookup_field = 'id'


class AllComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDetail(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    pagination_class = AdminApiPageNumber
    queryset = Comment.objects.all()
    lookup_field = 'id'


# TODO: Reported comments
class ReportedConfessions(CommentMixin):
    pass


# TODO: Blocked comments
class BlockedConfessions(CommentMixin):
    pass
