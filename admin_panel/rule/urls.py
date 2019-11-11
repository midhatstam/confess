from django.urls import path

from admin_panel.rule.views import RuleView

urlpatterns = [
    path('rules/', RuleView.as_view({'get': 'list', 'post': 'create', 'patch': 'update'})),
]
