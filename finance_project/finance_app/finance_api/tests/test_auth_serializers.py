import logging
from datetime import timedelta
from .base_test_setup import BaseTestSetup
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from ..auth import TokenVerifyRedisSerializer, RefreshTokenRedisSerializer

logger = logging.getLogger("__name__")


class TokenVerifyRedisSerializerTest(BaseTestSetup):
    def test_expired_token_is_not_verified(self):
        """
        Assert that expired token is not verified by verify serializer
        """
        expired_token = AccessToken()
        expired_token.lifetime = timedelta(microseconds=1)
        serializer = TokenVerifyRedisSerializer(data={"token": expired_token})
        self.assertFalse(
            expr=serializer.is_valid(),
            msg="VerifySerializer did not recognize expired token",
        )

    def test_blacklisted_token_not_validates(self):
        """
        Assert that token that is is blacklisted is not verified by serializer
        """
        creds = self.login_user(self.username_user_1)
        response = self.client.post(
            self.logout_url,
            headers={"Authorization": f"Bearer {creds["access"]}"},
            data={
                "refresh": creds["refresh"],
                "access": creds["access"],
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="Failed to logout test user before testing verifying blacklisted tokens",
        )
        serializer = TokenVerifyRedisSerializer(data={"token": creds["access"]})
        self.assertFalse(
            expr=serializer.is_valid(),
            msg="VerifySerializer did not recognize blacklisted access token",
        )
        serializer = TokenVerifyRedisSerializer(data={"token": creds["refresh"]})
        self.assertFalse(
            expr=serializer.is_valid(),
            msg="VerifySerializer did not recognize blacklisted refresh token",
        )

    def test_invalid_format_token_is_not_valid(self):
        """
        Assert that token that is not formatted right is not validated
        """
        invalid_token = "eyJhbGciOifI1NfcCI6IkpXVCJ9.eyJfjoiYWNjZXNzIiwiZXhwIjoxNzMxNTE3MDQ4LCJpYXQiOjE3MzE1MTYzODcsImp0aSI6IjNjYTI0OGfRiYzRmMjQ4MzNlNGQ5ZDUyMzlhODdiIiwidXNlcl9pZCI6MTd9.oULzTEK22JKQidnlHywC_Rms287DXAIj1uOM_lKNw8E"
        serializer = TokenVerifyRedisSerializer(data={"token": invalid_token})
        self.assertFalse(
            expr=serializer.is_valid(),
            msg="VerifySerializer did not recognize incorrect token",
        )


class TokenRefreshRedisSerializerTest(BaseTestSetup):
    """
    Test RefreshTokenRedisSerializer
    """

    def test_access_cant_be_used_for_refreshing(self):
        """
        Assert that access token cant be used for refreshing
        """
        creds = self.login_user(self.username_user_1)
        serializer = RefreshTokenRedisSerializer(data={"access": creds["access"]})
        self.assertFalse(
            expr=serializer.is_valid(),
            msg="RefreshSerializer did not differentiate access token from refresh token",
        )
