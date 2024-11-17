import logging
from django.test.client import RequestFactory
from .base_auth_test_setup import BaseAuthTestSetup
from ...auth.authentication import RedisJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from ...models import User

logger = logging.getLogger("__name__")


class RedisJWTAuthenticationTest(BaseAuthTestSetup):
    """
    Test RefreshTokenRedisSerializer
    """

    def test_blacklisted_token_cant_be_used_for_auth(self):
        """
        Assert that blacklisted token can't be used for request authentication
        """
        logged_out_creds = self.get_logged_out_tokens(self.username_user_1)
        auth_middleware = RedisJWTAuthentication()

        rf = RequestFactory()
        # mocking request with logged out tokens
        get = rf.get(
            "test/get/request",
            headers={"Authorization": f"Bearer {logged_out_creds["access"]}"},
        )
        with self.assertRaises(
            AuthenticationFailed,
            msg="JWT authentication middleware did not raise AuthenticationFailed \
                exception after trying to authenticate blacklisted token",
        ):
            auth_middleware.authenticate(request=get)

    def test_access_token_can_be_used_for_auth(self):
        """
        Assert that token types not stated in `settings.SIMPLE_JWT.AUTH_TOKEN_CLASSES`
        can't be used for authenticating requests. By default (which is used here),
        only access tokens can be used for auth, while refresh tokens can be
        used only for getting new access tokens
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
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
                msg="JWT authentication middleware authenticated request \
                    with access token, but did not return instance of User model ",
            )
            self.assertIsInstance(
                auth_result[1],
                AccessToken,
                msg="JWT authentication middleware authenticated request \
                    with access token, but did not return instance of AccessToken model ",
            )
        except Exception as e:
            self.fail(e)
    
    def test_refresh_token_cant_be_used_for_auth(self):
        """
        Assert that token types not stated in `settings.SIMPLE_JWT.AUTH_TOKEN_CLASSES`
        can't be used for authenticating requests. By default (which is used here),
        only access tokens can be used for auth, while refresh tokens can be
        used only for getting new access tokens
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        auth_middleware = RedisJWTAuthentication()

        rf = RequestFactory()
        # mocking request with refresh token instead of access token
        get = rf.get(
            "test/get/request",
            headers={"Authorization": f"Bearer {creds["refresh"]}"},
        )

        with self.assertRaises(
            AuthenticationFailed,
            msg="JWT authentication middleware authenticated request with \
                refresh token, but only access token is allowed ",
        ):
            auth_middleware.authenticate(request=get)
