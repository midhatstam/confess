from django.urls import path
from admin_panel.comment.views import *

urlpatterns = [
    path('comments/', AllComments.as_view()),
    path('comments/<int:id>/', CommentDetail.as_view()),
]
