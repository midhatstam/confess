from django.urls import path
from admin_panel.confession.views import *

urlpatterns = [
    path('confessions/', AllConfessions.as_view({'get': 'list', 'patch': 'update'})),
    path('confessions/admin-approved/', AdminApprovedConfessions.as_view({'get': 'list', 'patch': 'update'})),
    path('confessions/user-approved/', UserApprovedConfessions.as_view({'get': 'list', 'patch': 'update'})),
    path('confessions/unapproved/', UnapprovedConfessions.as_view({'get': 'list', 'patch': 'update'})),
    path('confessions/reported/', ReportedConfessions.as_view({'get': 'list', 'patch': 'update'})),
    path('confessions/<int:id>/', ConfessionDetail.as_view({'get': 'retrieve'})),
    path('confessions/for-approve/', ConfessionForApproveView.as_view({'get': 'list'})),
]
