from django.urls import path
from reports import views as reports_views

urlpatterns = [
    path('api/reports/<int:id>/', reports_views.ReportCommentAPI.as_view({'get': 'list', 'post': 'create'})),
]
