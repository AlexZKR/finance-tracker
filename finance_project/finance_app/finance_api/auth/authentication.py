from typing import Union, Tuple

import logging

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from ..models import User

from .jwt_blacklist import JWTMixin


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
        If no `Authorization` header is provided, sets the user to `django.contrib.auth.models.AnonymousUser`.

        For authorization to work must not handle `AuthenticationFailed` exceptions.
        """
        try:
            token = self.jwt_mixin.get_token(request=request)
            if token:
                if not self.jwt_mixin.is_token_allowed_for_auth(token):
                    raise AuthenticationFailed(
                        "Provided token is not allowed for authentication. Please provide correct token."
                    )
                if self.jwt_mixin.is_in_blacklist(token):
                    raise AuthenticationFailed(
                        "Token is blacklisted. Please log in again."
                    )
                return super().authenticate(request)
            else:
                return AnonymousUser(), None
        except TokenError as e:
            raise AuthenticationFailed(e)
