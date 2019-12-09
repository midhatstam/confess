from django.urls import path

from confession import views as confession_views

urlpatterns = [
	path('api/confessions/', confession_views.ConfessionApiView.as_view({'get': 'list', 'post': 'create'})),
	# path('api/confessions/<int:id>/', confession_views.ConfessionApiView.as_view({'patch': 'patch'})),
	path('api/confessions/popular/', confession_views.ConfessionApiPopularView.as_view({'get': 'list'})),
	path('api/confessions/best/', confession_views.ConfessionApiBestView.as_view({'get': 'list'})),
	path('api/confessions/by-comments/', confession_views.ConfessionApiMostCommentsView.as_view({'get': 'list'})),
	path('api/confessions/by-likes/', confession_views.ConfessionApiMostLikeView.as_view({'get': 'list'})),
	path('api/confessions/by-dislikes/', confession_views.ConfessionApiMostDislikeView.as_view({'get': 'list'})),
	path('api/confessions/approve/', confession_views.ConfessionApiForApprove.as_view({'get': 'retrieve'})),
	path('api/confessions/send-approvement/', confession_views.ConfessionUserApprovementView.as_view({'post': 'create'}), name='send-approvement'),
]
