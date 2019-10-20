from django.conf.urls import url
from admin.comment.views import *

urlpatterns = [
    url(r'comments/$', AllComments.as_view()),
    url(r'comments/(?P<id>[0-9]+)/$', CommentDetail.as_view()),
]
