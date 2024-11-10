from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BaseCategoryViewSet,
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    UserCategoryViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"accounts", AccountViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"user_categories", UserCategoryViewSet)
router.register(r"base_categories", BaseCategoryViewSet)


urlpatterns = [path("", include(router.urls))]
