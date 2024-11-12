from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .jwt_blacklist import JWTBlackList


class RefreshTokenRedisSerializer(serializers.Serializer):
    """
    Custom refresh token serializer that checks Redis cache
    before returning new access token
    """

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]):
        refresh = self.token_class(attrs["refresh"])
        if JWTBlackList().check_blacklist(refresh.token):
            raise serializers.ValidationError(
                {"refresh": "Refresh token is blacklisted."}
            )
        data = {"access": str(refresh.access_token)}
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        return data
