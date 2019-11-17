from rest_framework import pagination, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rule.models import Rule
from rule.serializers import RuleSerializer


class AdminApiPageNumber(pagination.PageNumberPagination):
    page_size = 25


class RuleView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    pagination_class = AdminApiPageNumber
    lookup_field = 'id'
