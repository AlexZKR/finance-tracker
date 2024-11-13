from typing import Union, Tuple

import logging

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from ..models import User

from .jwt_blacklist import JWTMixin
from ..utils import get_auth_token_class_objects

logger = logging.getLogger(__name__)


class RedisJWTAuthentication(JWTAuthentication):
    """Custom authentication class using Redis JWT caching"""

    def __init__(self):
        super().__init__()
        self.jwt_mixin = JWTMixin()

    def authenticate(
        self, request
    ) -> Union[Tuple[AnonymousUser, None], Tuple[User, AccessToken]]:
        """
        Authenticates requests by `Authorization` header.
        If token is not allowed for authentication or is blacklisted in redis
        throws `AuthenticationFailed` exception.
        If no `Authorization` header is provided, sets the user to `django.contrib.auth.models.AnonymousUser`
        """

        token = self.get_token(request=request)
        if token:
            if not self.is_token_allowed_for_auth(token):
                raise AuthenticationFailed(
                    "Provided token is not allowed for authentication. Please provide correct token."
                )
            if self.is_token_blacklisted(token):
                raise AuthenticationFailed("Token is blacklisted. Please log in again.")
            return super().authenticate(request)
        else:
            return AnonymousUser(), None

    def get_token(self, request):
        """
        Checks request headers for `Authorization` header and returns it contents.
        Returns `None` if header does not exist
        """
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split(" ")[1]
            return token
        return None

    def is_token_allowed_for_auth(self, token):
        """
        Asserts that token is of type that is configured to use
        to authenticate requests in `settings.SIMPLE_JWT.AUTH_TOKEN_CLASSES`
        """
        token_type = self.jwt_mixin.get_token_type(token)
        token_instance = self.jwt_mixin.instantiate_token(token_type, token)

        class_objects = get_auth_token_class_objects()

        if not isinstance(token_instance, tuple(class_objects)):
            return False

        return True

    def is_token_blacklisted(self, access_token):
        """
        Checks if token is in blacklist. If yes, returns `True`
        """
        is_blacklisted = self.jwt_mixin.is_in_blacklist(access_token)
        if is_blacklisted:
            return True
        return False
