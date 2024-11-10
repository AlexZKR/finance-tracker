from .models import Account, BaseCategory, Transaction, User, UserCategory
from .serializers import (
    AccountSerializer,
    BaseCategorySerializer,
    TransactionSerializer,
    UserSerializer,
    UserCategorySerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
    )
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=request.data["email"],
                password=request.data["password"],
                username=request.data["username"],
            )
            user.save()
            return Response(
                data="User created successfully",
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="logout")
    def logout(self, request):
        try:
            refresh_token = RefreshToken(request.data["refresh"])
            refresh_token.blacklist()
            return Response(
                data="User logout successful", status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_400_BAD_REQUEST)


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrAdmin]

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
