from django.conf.urls import url
from voting import views as voting_views

urlpatterns = [
	url(r'^api/confessions/voting/up/$', voting_views.VoteMixin.as_view({'post': 'up'})),
]
