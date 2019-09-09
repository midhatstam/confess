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
from core import views

urlpatterns = [
    url(r'^$', views.ConfessView.as_view({'get': 'list', 'post': 'create'}), name='home'),
    url(r'^popular/$', views.ConfessPopularView.as_view({'get': 'list'})),
    url(r'^best/$', views.ConfessBestView.as_view({'get': 'list'})),
    url(r'^by_comments/$', views.ConfessMostCommentsView.as_view({'get': 'list'})),
    url(r'^by_likes/$', views.ConfessMostLikeView.as_view({'get': 'list'})),
    url(r'^by_dislikes/$', views.ConfessMostDislikeView.as_view({'get': 'list'})),
    url(r'^api/confesses/$', views.ConfessApiView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^api/confesses/(?P<id>[0-9]+)/$', views.ConfessApiView.as_view({'get': 'retrieve', 'put': 'patch'})),
    url(r'^api/confesses/popular/$', views.ConfessApiPopularView.as_view({'get': 'list'})),
    url(r'^api/confesses/best/$', views.ConfessApiBestView.as_view({'get': 'list'})),
    url(r'^api/confesses/by_comments/$', views.ConfessApiMostCommentsView.as_view({'get': 'list'})),
    url(r'^api/confesses/by_likes/$', views.ConfessApiMostLikeView.as_view({'get': 'list'})),
    url(r'^api/confesses/by_dislikes/$', views.ConfessApiMostDislikeView.as_view({'get': 'list'})),
    url(r'^admin/', admin.site.urls),
    # url(r'^confesses/$', views.ConfessView.as_view()),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns