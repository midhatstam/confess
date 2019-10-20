from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('admin.confession.urls'), name='admin-confessions'),
    url(r'', include('admin.comment.urls'), name='admin-comments'),
]
