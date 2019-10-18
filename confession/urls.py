from django.conf.urls import url

from confession import views as confession_views

urlpatterns = [
	url(r'^api/confessions/$', confession_views.ConfessionApiView.as_view({'get': 'list', 'post': 'create'})),
	url(r'^api/confessions/(?P<id>[0-9]+)/$', confession_views.ConfessionApiView.as_view({'patch': 'patch'})),
	url(r'^api/confessions/popular/$', confession_views.ConfessionApiPopularView.as_view({'get': 'list'})),
	url(r'^api/confessions/best/$', confession_views.ConfessionApiBestView.as_view({'get': 'list'})),
	url(r'^api/confessions/by_comments/$', confession_views.ConfessionApiMostCommentsView.as_view({'get': 'list'})),
	url(r'^api/confessions/by_likes/$', confession_views.ConfessionApiMostLikeView.as_view({'get': 'list'})),
	url(r'^api/confessions/by_dislikes/$', confession_views.ConfessionApiMostDislikeView.as_view({'get': 'list'})),
]
