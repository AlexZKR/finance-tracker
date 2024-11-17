from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BaseCategoryViewSet,
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    UserCategoryViewSet,
    LoginView,
    LogoutView,
    RefreshView,
    VerifyView,
)
from rest_framework.permissions import AllowAny

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"transactions", TransactionViewSet)
router.register(r"user_categories", UserCategoryViewSet)
router.register(r"base_categories", BaseCategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/login", LoginView.as_view(), name="login"),
    path(
        "auth/register",
        UserViewSet.as_view({"post": "register"}, permission_classes=[AllowAny]),
        name="register",
    ),
    path("auth/refresh", RefreshView.as_view(), name="refresh"),
    path("auth/verify", VerifyView.as_view(), name="verify"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
