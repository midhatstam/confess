from django.urls import path
from voting import views as voting_views

urlpatterns = [
	path('api/voting/up/', voting_views.VoteMixin.as_view({'post': 'up'})),
]
