from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"transactions", views.TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
