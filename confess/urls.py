"""confess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from core import views as core_views
import confession.utils as con_utils

urlpatterns = [
    path('', core_views.ConfessionView.as_view({'get': 'list', 'post': 'create'}), name='home'),
    path('', include('core.urls')),
    path('', include('confession.urls')),
    path('', include('vote.urls')),
    path('', include('voting.urls')),
    path('', include('comment.urls')),
    path('', include('reports.urls')),
    path('admin/', admin.site.urls),
    path('adminpanel/', include('admin_panel.urls')),
    path('instagram/', con_utils.instagram),
    # path('confesses/', views.ConfessView.as_view()),

]

# if settings.DEBUG:
# import debug_toolbar
#
# urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
