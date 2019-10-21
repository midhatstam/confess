from django.urls import path
from admin.confession.views import *

urlpatterns = [
    path('confessions/', AllConfessions.as_view()),
    path('confessions/admin-approved/', AdminApprovedConfessions.as_view()),
    path('confessions/user-approved/', UserApprovedConfessions.as_view()),
    path('confessions/unapproved/', UnapprovedConfessions.as_view()),
    path('confessions/<int:id>/', ConfessionDetail.as_view()),
]
