from django.conf.urls import url

from core import views as core_views

urlpatterns = [
	
	url(r'^popular/$', core_views.ConfessPopularView.as_view({'get': 'list'})),
	url(r'^best/$', core_views.ConfessBestView.as_view({'get': 'list'})),
	url(r'^by_comments/$', core_views.ConfessMostCommentsView.as_view({'get': 'list'})),
	url(r'^by_likes/$', core_views.ConfessMostLikeView.as_view({'get': 'list'})),
	url(r'^by_dislikes/$', core_views.ConfessMostDislikeView.as_view({'get': 'list'})),
	url(r'^api/confesses/$', core_views.ConfessApiView.as_view({'get': 'list', 'post': 'create'})),
	url(r'^api/confesses/(?P<id>[0-9]+)/$', core_views.ConfessApiView.as_view({'get': 'retrieve', 'put': 'patch'})),
	url(r'^api/confesses/popular/$', core_views.ConfessApiPopularView.as_view({'get': 'list'})),
	url(r'^api/confesses/best/$', core_views.ConfessApiBestView.as_view({'get': 'list'})),
	url(r'^api/confesses/by_comments/$', core_views.ConfessApiMostCommentsView.as_view({'get': 'list'})),
	url(r'^api/confesses/by_likes/$', core_views.ConfessApiMostLikeView.as_view({'get': 'list'})),
	url(r'^api/confesses/by_dislikes/$', core_views.ConfessApiMostDislikeView.as_view({'get': 'list'})),
]
