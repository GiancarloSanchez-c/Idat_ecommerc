from django.urls import path
from .views import RegisterInfoView
urlpatterns = [
    path('info/', RegisterInfoView.as_view(), name='info'),
]
