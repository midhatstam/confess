from django.conf.urls import url
from admin.confession.views import *

urlpatterns = [
    url(r'confessions/$', AllConfessions.as_view()),
    url(r'confessions/admin-approved/$', AdminApprovedConfessions.as_view()),
    url(r'confessions/user-approved/$', UserApprovedConfessions.as_view()),
    url(r'confessions/unapproved/$', UnapprovedConfessions.as_view()),
    url(r'confessions/(?P<id>[0-9]+)/$', ConfessionDetail.as_view()),
]
