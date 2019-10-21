from django.urls import path
from admin.comment.views import *

urlpatterns = [
    path('comments/', AllComments.as_view()),
    path('comments/<int:id>/', CommentDetail.as_view()),
]
