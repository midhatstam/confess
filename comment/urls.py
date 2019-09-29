from django.conf.urls import url
from comment import views as comment_views

urlpatterns = [
	url(r'^api/confessions/(?P<id>[0-9]+)/comments/$', comment_views.CommentApiMixin.as_view({'get': 'list', 'post': 'create'})),
	url(r'^api/confessions/(?P<id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$', comment_views.CommentDetailsApiMixin.as_view({'get': 'list', 'post': 'create'}))
]
