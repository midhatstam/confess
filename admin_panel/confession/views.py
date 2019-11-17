from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from confession.models import Confession, AllConfession, ApprovedConfession, AdminApprovedConfession, \
    ReportedConfession, ConfessionForApprove
from confession.serializers import ConfessionSerializer


class AdminApiPageNumber(pagination.PageNumberPagination):
    page_size = 25


class ConfessionMixin(viewsets.ModelViewSet):
    serializer_class = ConfessionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AdminApiPageNumber
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = AllConfession.objects.filter(id=request.data['id']).first()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AllConfessions(ConfessionMixin):
    queryset = AllConfession.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = AdminApiPageNumber


class AdminApprovedConfessions(ConfessionMixin):
    permission_classes = (IsAuthenticated,)
    queryset = AdminApprovedConfession.objects.all()


class UserApprovedConfessions(ConfessionMixin):
    permission_classes = (IsAuthenticated,)
    queryset = ApprovedConfession.objects.all()


class UnapprovedConfessions(ConfessionMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Confession.objects.filter(admin_approved=False, user_approved=False)


class ConfessionDetail(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConfessionSerializer
    queryset = Confession.objects.all()
    lookup_field = 'id'


class ReportedConfessions(ConfessionMixin):
    permission_classes = (IsAuthenticated,)
    queryset = ReportedConfession.objects.all()


class ConfessionForApproveView(ConfessionMixin):
    permission_classes = (IsAuthenticated,)
    queryset = ConfessionForApprove.objects.all()
