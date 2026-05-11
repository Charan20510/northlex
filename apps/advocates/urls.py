from django.urls import path
from . import views

app_name = 'advocates'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
