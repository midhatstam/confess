from rest_framework import pagination, viewsets

from rule.models import Rule
from rule.serializers import RuleSerializer


class AdminApiPageNumber(pagination.PageNumberPagination):
    page_size = 25


class RuleView(viewsets.ModelViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    pagination_class = AdminApiPageNumber
    lookup_field = 'id'
