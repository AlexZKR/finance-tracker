from datetime import timedelta

from .base_auth_test_setup import BaseAuthTestSetup
from ...auth import JWTMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class JWTBlackListMixinTest(BaseAuthTestSetup):
    """
    Test JWT blacklist mixin logic
    """

    def test_expired_token_raises_exception_when_tested_for_auth_eligibility(self):
        """
        Assert that expired token raises AuthenticationFailed when provided for auth
        """
        expired_token = AccessToken()
        expired_token.lifetime = timedelta(microseconds=1)
        mixin = JWTMixin()

        with self.assertRaises(
            TokenError,
            msg="JWT mixin did not raise TokenError after \
                providing one expired token",
        ):
            mixin.is_token_allowed_for_auth(expired_token)

    def test_expired_token_raises_exception_when_tested_for_auth_elegebility(self):
        """
        Assert that expired token can't be blacklisted by mixin
        """
        expired_token = AccessToken()
        expired_token.lifetime = timedelta(microseconds=1)
        mixin = JWTMixin()

        with self.assertRaises(
            TokenError,
            msg="JWT mixin did not raise TokenError after \
                providing one expired token",
        ):
            mixin.blacklist_tokens(expired_token)

    def test_not_valid_token_raises_exception_when_blacklisted(self):
        """
        Assert that not valid single token can't be blacklisted by mixin
        """
        invalid_token = "eyJhbGciOi1235cCI6IkpXVCJ9.eyJ0b2tl123zIiwiZXhwIjo3MzQ3LCJpYXQiOjE3MzE1ODk3NDcsImp0aSI6IjUwMzQwZDJkZjIzNjRjZjFhOWRlNzdkMDY4ZGQ2Mzljfff.oNIcxPA2GsKbff"
        mixin = JWTMixin()

        with self.assertRaises(
            TokenError,
            msg="JWT mixin did not raise TokenError after \
                providing one invalid token",
        ):
            mixin.blacklist_tokens(invalid_token)

    def test_access_refresh_valid_tokens_can_be_blacklisted(self):
        """
        Assert that two valid tokens (access, refresh) can be blacklisted by mixin
        """
        valid_creds = self.get_logged_in_tokens(self.username_user_1)
        mixin = JWTMixin()

        self.assertTrue(
            mixin.blacklist_tokens(valid_creds["refresh"], valid_creds["access"]),
            msg="JWT mixin did not return True after \
                blacklisting two valid tokens (access, refresh)",
        )

    def test_one_valid_refresh_token_can_be_blacklisted(self):
        """
        Assert that one valid refresh token can be blacklisted by mixin
        """
        valid_creds = self.get_logged_in_tokens(self.username_user_1)
        mixin = JWTMixin()

        self.assertTrue(
            mixin.blacklist_tokens(valid_creds["refresh"]),
            msg="JWT mixin did not return True after \
                blacklisting one valid refresh token",
        )

    def test_one_valid_access_token_can_be_blacklisted(self):
        """
        Assert that one valid access token can be blacklisted by mixin
        """
        valid_creds = self.get_logged_in_tokens(self.username_user_1)
        mixin = JWTMixin()

        self.assertTrue(
            mixin.blacklist_tokens(valid_creds["access"]),
            msg="JWT mixin did not return True after \
                blacklisting one valid access token",
        )
