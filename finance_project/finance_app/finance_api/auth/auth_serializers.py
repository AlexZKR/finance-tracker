import logging
from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError
from .jwt_blacklist import JWTMixin

logger = logging.getLogger("__name__")


class TokenVerifyRedisSerializer(serializers.Serializer):
    """
    Custom serializer that verifies any tokens for:
    1) invalid format
    2) expiration time
    3) being blacklisted in redis
    """

    token = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, None]) -> Dict[Any, Any]:
        try:
            token = UntypedToken(attrs["token"])
            if JWTMixin().is_in_blacklist(token):
                raise serializers.ValidationError(
                    {"verify error": "Token is blacklisted."}
                )
            return {"detail": "Token is valid"}
        except TokenError as e:
            raise serializers.ValidationError({"verify error": e})


class RefreshTokenRedisSerializer(serializers.Serializer):
    """
    Custom refresh token serializer that validates refresh token's:
    1) for invalid format
    2) for expiration
    3) for beind in redis blacklist
    """

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]):
        refresh = self.token_class(attrs["refresh"])
        if JWTMixin().is_in_blacklist(refresh.token):
            raise serializers.ValidationError(
                {"refresh": "Refresh token is blacklisted."}
            )
        data = {"access": str(refresh.access_token)}
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        return data
