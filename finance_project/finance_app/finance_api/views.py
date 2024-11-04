from .models import Account, BaseCategory, Transaction, User, UserCategory
from .serializers import (
    AccountSerializer,
    BaseCategorySerializer,
    TransactionSerializer,
    UserSerializer,
    UserCategorySerializer,
)
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserCategoryViewSet(ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer


class BaseCategoryViewSet(ModelViewSet):
    queryset = BaseCategory.objects.all()
    serializer_class = BaseCategorySerializer
