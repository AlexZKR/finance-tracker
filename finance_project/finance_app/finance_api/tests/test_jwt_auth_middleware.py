import logging
from django.test.client import RequestFactory
from .base_test_setup import BaseTestSetup
from ..auth.authentication import RedisJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from ..models import User


class RedisJWTAuthenticationTest(BaseTestSetup):
    """
    Test RefreshTokenRedisSerializer
    """

    # TODO: test blacklisting, test JWT blacklist mixin
    def test_access_token_can_be_used_for_auth(self):
        """
        Assert that token types not stated in `settings.SIMPLE_JWT.AUTH_TOKEN_CLASSES` can't be
        used for authenticating requests. By default (which is used here),
        only access tokens can be used for auth, while refresh tokens can be
        used only for getting new access tokens
        """
        creds = self.login_user(self.username_user_1)
        auth_middleware = RedisJWTAuthentication()

        rf = RequestFactory()
        # mocking request with refresh token instead of access token
        get = rf.get(
            "test/get/request",
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        try:
            auth_result = auth_middleware.authenticate(request=get)
            self.assertIsInstance(
                auth_result[0],
                User,
                msg="JWT authentication middleware authenticated request with access token, but did not return instance of User model ",
            )
            self.assertIsInstance(
                auth_result[1],
                AccessToken,
                msg="JWT authentication middleware authenticated request with access token, but did not return instance of AccessToken model ",
            )
        except Exception as e:
            self.fail(e)

    def test_refresh_token_cant_be_used_for_auth(self):
        """
        Assert that token types not stated in `settings.SIMPLE_JWT.AUTH_TOKEN_CLASSES` can't be
        used for authenticating requests. By default (which is used here),
        only access tokens can be used for auth, while refresh tokens can be
        used only for getting new access tokens
        """
        creds = self.login_user(self.username_user_1)
        auth_middleware = RedisJWTAuthentication()

        rf = RequestFactory()
        # mocking request with refresh token instead of access token
        get = rf.get(
            "test/get/request",
            headers={"Authorization": f"Bearer {creds["refresh"]}"},
        )

        with self.assertRaises(
            AuthenticationFailed,
            msg="JWT authentication middleware authenticated request with refresh token, but only access token is allowed ",
        ):
            auth_middleware.authenticate(request=get)
