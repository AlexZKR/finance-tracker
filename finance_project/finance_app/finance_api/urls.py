from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BaseCategoryViewSet,
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    UserCategoryViewSet,
    CustomLoginView,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.schemas import get_schema_view


router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"transactions", TransactionViewSet)
router.register(r"user_categories", UserCategoryViewSet)
router.register(r"base_categories", BaseCategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/login", CustomLoginView.as_view(), name="login"),
    path(
        "auth/register",
        UserViewSet.as_view({"post": "register"}, permission_classes=[AllowAny]),
        name="register",
    ),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "openapi",
        get_schema_view(
            title="Personal finance tracker app",
            description="Finance tracker API",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
]
