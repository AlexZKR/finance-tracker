import logging
from ..models import Account, BaseCategory, Transaction, UserCategory
from ..serializers import (
    AccountSerializer,
    BaseCategorySerializer,
    TransactionSerializer,
    UserCategorySerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from ..auth import IsOwnerOrAdmin


logger = logging.getLogger("__name__")


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this resource.")
        if self.request.user.is_staff:
            return Account.objects.all()
        return Account.objects.filter(user=self.request.user)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserCategoryViewSet(ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer


class BaseCategoryViewSet(ModelViewSet):
    queryset = BaseCategory.objects.all()
    serializer_class = BaseCategorySerializer
