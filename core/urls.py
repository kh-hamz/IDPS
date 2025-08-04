from django.urls import path
from . import views

app_name = 'core'  # <== This is important for namespace to work

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_view, name='settings'),
]