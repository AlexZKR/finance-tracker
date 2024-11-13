import logging
from django.core.cache import cache
from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


logger = logging.getLogger("__name__")


class JWTMixin:
    def blacklist_tokens(self, *args):
        """
        Blacklists any number of provided tokens in redis cache
        """
        for token in args:
            token_type = self.get_token_type(token)
            token_class = self.instantiate_token(token_type, token)

            exp_time = int(token_class.lifetime.total_seconds())
            result = cache.set(key=token, value="blacklisted", timeout=exp_time)
            if not result:
                logger.error(f"Failed to cache token {token} to Redis.")
                return False
        return True

    def instantiate_token(self, token_type, token_string):
        """
        Get an instance of one of rest_framework_simplejwt.tokens classes using token_type
        """
        if token_type == "access":
            return AccessToken(token_string)
        if token_type == "refresh":
            return RefreshToken(token_string)

    def is_token_type(self, token, provided_type) -> bool:
        """
        Check if provided token is of provided type.
        If not return `False`
        """
        true_type = self.get_token_type(token)
        return provided_type == true_type

    def get_token_type(self, token_string):
        """
        Decode token to get `token_type` field and get type of token
        """
        try:
            token = UntypedToken(token_string)
            token_type = token.payload.get(settings.SIMPLE_JWT["TOKEN_TYPE_CLAIM"])
            return token_type
        except TokenError:
            return None

    def is_in_blacklist(self, token):
        """Return `True` if token is in Redis blacklist"""
        if cache.get(token):
            return True
        return False
