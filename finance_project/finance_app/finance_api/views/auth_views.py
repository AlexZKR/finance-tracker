import logging

from ..serializers import UserSerializer
from ..models import User
from ..auth import JWTBlackList, RedisJWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet

logger = logging.getLogger("__name__")


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [RedisJWTAuthentication]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            access_token = request.data.get("access")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not access_token:
                return Response(
                    {"detail": "Access token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            are_blacklisted = JWTBlackList().blacklist_tokens(
                access_token, refresh_token
            )
            if are_blacklisted:
                return Response(
                    {"detail": "Logout successful"},
                    status=status.HTTP_204_NO_CONTENT,
                )

        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
