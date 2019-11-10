from django.urls import path

from core import views as core_views

urlpatterns = [
	
	path('popular/', core_views.ConfessionPopularView.as_view({'get': 'list'})),
	path('best/', core_views.ConfessionBestView.as_view({'get': 'list'})),
	path('by-comments/', core_views.ConfessionMostCommentsView.as_view({'get': 'list'})),
	path('by-likes/', core_views.ConfessionMostLikeView.as_view({'get': 'list'})),
	path('by-dislikes/', core_views.ConfessionMostDislikeView.as_view({'get': 'list'})),
]
