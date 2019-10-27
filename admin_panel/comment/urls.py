from django.urls import path
from admin_panel.comment.views import *

urlpatterns = [
    path('comments/', AllComments.as_view({'get': 'list', 'patch': 'update'})),
    path('comments/reported/', ReportedComments.as_view({'get': 'list', 'patch': 'update'})),
    path('comments/reported/reports/', CommentReports.as_view({'get': 'reports'})),
    path('comments/<int:id>/', CommentDetail.as_view({'get': 'list'})),
]
