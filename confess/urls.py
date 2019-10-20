"""confess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from core import views as core_views

urlpatterns = [
	url(r'^$', core_views.ConfessionView.as_view({'get': 'list', 'post': 'create'}), name='home'),
	url(r'^', include('core.urls')),
	url(r'^', include('confession.urls')),
	url(r'^', include('vote.urls')),
	url(r'^', include('voting.urls')),
	url(r'^', include('comment.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^adminpanel/', include('admin.urls'))
	# url(r'^confesses/$', views.ConfessView.as_view()),

]

if settings.DEBUG:
	# import debug_toolbar
	#
	# urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
	urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
