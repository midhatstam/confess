from django.urls import path, include

urlpatterns = [
    path('', include('admin_panel.confession.urls'), name='admin-confessions'),
    path('', include('admin_panel.comment.urls'), name='admin-comments'),
]
