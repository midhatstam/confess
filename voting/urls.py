from django.conf.urls import url
from voting import views as voting_views

urlpatterns = [
	url(r'^api/voting/up/$', voting_views.VoteMixin.as_view({'post': 'up'})),
]
