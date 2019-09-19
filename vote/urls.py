from django.conf.urls import url
from vote import views as vote_views

urlpatterns = [
	url(r'^api/confessions/vote/up/$', vote_views.ConfessionVoteMixin.as_view({'post': 'up'})),
	url(r'^api/comments/vote/up/$', vote_views.CommentVoteMixin.as_view({'post': 'up'})),
]
