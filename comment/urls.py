from django.urls import path
from comment import views as comment_views

urlpatterns = [
    path('api/confessions/<int:id>/comments/',
         comment_views.CommentApiMixin.as_view({'get': 'list', 'post': 'create'}),
         name='comments'),
    path('api/confessions/<int:id>/comments/<int:comment_id>/',
         comment_views.CommentDetailsApiMixin.as_view({'get': 'list', 'post': 'create'}),
         name='comment-replies')
]
