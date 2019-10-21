from django.urls import path
from vote import views as vote_views

urlpatterns = [
	path('api/confessions/vote/up/', vote_views.ConfessionVoteMixin.as_view({'post': 'up'})),
	path('api/comments/vote/up/', vote_views.CommentVoteMixin.as_view({'post': 'up'})),
]
