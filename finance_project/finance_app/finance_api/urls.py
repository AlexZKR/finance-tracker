from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"categories", CategoryViewSet)



urlpatterns = [path("", include(router.urls))]