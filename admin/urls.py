from django.urls import path, include

urlpatterns = [
    path('', include('admin.confession.urls'), name='admin-confessions'),
    path('', include('admin.comment.urls'), name='admin-comments'),
]
