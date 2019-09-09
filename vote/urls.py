from django.conf.urls import url
from vote import views as vote_views

urlpatterns = [
	url(r'^api/confesses/vote/up/$', vote_views.ConfessVoteMixin.as_view({'post': 'up'})),
	url(r'^api/comments/vote/up/$', vote_views.CommentVoteMixin.as_view({'post': 'up'})),
	url(r'^api/comments/vote/down/$', vote_views.CommentVoteMixin.as_view({'post': 'down'})),
]
