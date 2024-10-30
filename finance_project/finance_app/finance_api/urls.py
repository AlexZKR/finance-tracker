from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path("", views.api_root),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetailed.as_view(), name="user-detail"),
    path("accounts/", views.AccountList.as_view(), name="account-list"),
    path("accounts/<int:pk>", views.AccountDetailed.as_view(), name="account-detail"),
]
