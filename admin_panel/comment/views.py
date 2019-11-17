from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import CommentSerializer
from confession.views import CustomApiPageNumber
from reports.models import ReportComment
from reports.serializers import ReportCommentSerializer


class AdminApiPageNumber(CustomApiPageNumber):
    page_size = 25


class CommentMixin(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = AdminApiPageNumber
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = Comment.objects.filter(id=request.data['id']).first()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AllComments(CommentMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.filter(reported=False)


class CommentDetail(CommentMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    lookup_field = 'id'


class ReportedComments(CommentMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.filter(reported=True)


class CommentReports(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportCommentSerializer

    def reports(self, request, *args, **kwargs):
        queryset = ReportComment.objects.filter(comment__id=request.data['id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
