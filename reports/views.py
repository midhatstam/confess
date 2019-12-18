from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from confession.utils import session_token
from confession.views import CustomApiPageNumber

from comment.models import Comment
from reports.serializers import ReportCommentSerializer
from reports.models import ReportComment


class ReportCommentAPI(viewsets.ModelViewSet):
    serializer_class = ReportCommentSerializer
    pagination_class = CustomApiPageNumber
    queryset = ReportComment.objects.all()
    lookup_field = 'id'

    @method_decorator(session_token)
    def list(self, request, *args, **kwargs):
        queryset = ReportComment.objects.filter(comment_id=kwargs['id']).order_by('-item_meta_data_date')
        serializer = ReportCommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(session_token)
    @action(methods=['POST', 'GET'], detail=False)
    def create(self, request, *args, **kwargs):
        comment = Comment.objects.filter(id=kwargs.pop('id'))
        if not comment.exists() or comment.count() != 1:
            raise ValidationError("This is not valid comment!")
        serializer = ReportCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comment=comment.first())
        return Response(serializer.data)
