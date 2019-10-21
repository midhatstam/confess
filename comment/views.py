from django.db.models import Prefetch, Count
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from confession.views import CustomApiPageNumber

from confession.models import Confession
from comment.models import Comment
from comment.serializers import CommentSerializer
from reports.models import ReportComment
from voting.models import Vote


class CommentApiMixin(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomApiPageNumber
    queryset = Comment.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(related_id=kwargs['id'], is_parent=True).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=5), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=5), to_attr='dislikes')
        ).annotate(report_count=Count("comments")).order_by('-item_meta_data_date')
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['POST', 'GET'])
    def create(self, request, *args, **kwargs):
        confess = Confession.objects.filter(id=kwargs.pop('id'))
        if not confess.exists() or confess.count() != 1:
            raise ValidationError("This is not valid confess!")
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(related=confess.first(), is_parent=1)
        return Response(serializer.data)


class CommentDetailsApiMixin(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomApiPageNumber
    queryset = Comment.objects.all()
    lookup_field = 'comment_id'

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(
            related_id=kwargs['id'],
            is_parent=False,
            parent_id=kwargs['comment_id']
        ).prefetch_related(
            Prefetch('votes', queryset=Vote.objects.filter(vote=1, content_type=5), to_attr='likes'),
            Prefetch('votes', queryset=Vote.objects.filter(vote=0, content_type=5), to_attr='dislikes')
        ).order_by('-item_meta_data_date')
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['POST', 'GET'])
    def create(self, request, *args, **kwargs):
        confess = Confession.objects.filter(id=kwargs.pop('id'))
        if not confess.exists() or confess.count() != 1:
            raise ValidationError("This is not valid confess!")
        comment_parent = Comment.objects.filter(id=kwargs.pop('comment_id'))
        if not comment_parent.exists() or comment_parent.count() != 1:
            raise ValidationError("This is not valid comment parent!")
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(related=confess.first(), parent=comment_parent.first())
        return Response(serializer.data)
