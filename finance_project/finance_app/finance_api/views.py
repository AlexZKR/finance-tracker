from .models import Account, Transaction, User, UserCategory
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    UserSerializer,
    CategorySerializer,
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


class CategoryViewSet(ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = CategorySerializer
