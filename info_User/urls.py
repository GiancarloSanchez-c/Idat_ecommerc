from django.urls import path
from .views import RegisterInfoView, UserListView
urlpatterns = [
    path('info/', RegisterInfoView.as_view(), name='info'),
    path('user_list', UserListView.as_view(), name='user')
]
