from rest_framework import pagination, generics

from confession.models import Confession
from confession.serializers import ConfessionSerializer


class AdminApiPageNumber(pagination.PageNumberPagination):
    page_size = 25


class ConfessionMixin(generics.ListAPIView):
    serializer_class = ConfessionSerializer
    pagination_class = AdminApiPageNumber
    lookup_field = 'id'


class AllConfessions(ConfessionMixin):
    queryset = Confession.objects.all()
    pagination_class = AdminApiPageNumber


class AdminApprovedConfessions(ConfessionMixin):
    queryset = Confession.objects.filter(admin_approved=True, user_approved=False)


class UserApprovedConfessions(ConfessionMixin):
    queryset = Confession.objects.filter(admin_approved=True, user_approved=True)


class UnapprovedConfessions(ConfessionMixin):
    queryset = Confession.objects.filter(admin_approved=False, user_approved=False)


class ConfessionDetail(generics.RetrieveAPIView):
    serializer_class = ConfessionSerializer
    pagination_class = AdminApiPageNumber
    queryset = Confession.objects.all()
    lookup_field = 'id'


# TODO: Reported confessions
class ReportedConfessions(ConfessionMixin):
    pass


# TODO: Blocked confessions
class BlockedConfessions(ConfessionMixin):
    pass
