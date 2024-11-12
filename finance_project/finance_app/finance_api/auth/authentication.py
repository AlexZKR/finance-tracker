import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt_blacklist import JWTBlackList

logger = logging.getLogger(__name__)


class RedisJWTAuthentication(JWTAuthentication):
    """Custom authentication class using Redis JWT caching"""

    def authenticate(self, request):
        access_token = request.headers.get("Authorization").split(" ")[1]
        is_blacklisted = JWTBlackList().check_blacklist(access_token)
        if is_blacklisted:
            raise AuthenticationFailed("Token is blacklisted. Please log in again.")
        return super().authenticate(request)
