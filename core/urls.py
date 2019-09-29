from django.conf.urls import url

from core import views as core_views

urlpatterns = [
	
	url(r'^popular/$', core_views.ConfessionPopularView.as_view({'get': 'list'})),
	url(r'^best/$', core_views.ConfessionBestView.as_view({'get': 'list'})),
	url(r'^by_comments/$', core_views.ConfessionMostCommentsView.as_view({'get': 'list'})),
	url(r'^by_likes/$', core_views.ConfessionMostLikeView.as_view({'get': 'list'})),
	url(r'^by_dislikes/$', core_views.ConfessionMostDislikeView.as_view({'get': 'list'})),
]
