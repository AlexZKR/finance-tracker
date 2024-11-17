import logging
from .base_auth_test_setup import BaseAuthTestSetup
from rest_framework import status

from django.core.cache import cache


logger = logging.getLogger("__name__")


class VerifyAuthEndpointTest(BaseAuthTestSetup):
    def test_verify_endpoint_is_authenticated_only(self):
        """
        Assert that verify endpoint is restricted only for authenticated users
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.verify_url,
            data={"refresh": creds["access"]},  # not providing auth header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_verify_case(self):
        """
        Assert that authenticated user can verify any token
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.verify_url,
            data={"token": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RefreshAuthEndpointTest(BaseAuthTestSetup):
    """
    Test refresh tokens endpoint
    """

    def test_refresh_is_authenticated_only(self):
        """
        Assert that refresh endpoint is restricted only for authenticated users
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.refresh_url,
            data={"refresh": creds["access"]},  # not providing auth header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg="When trying to access without auth header, valid refresh jwt endpoint did not return 403 forbidden",
        )

    def test_valid_refresh_case(self):
        """
        Assert that user can refresh his access token using refresh token
        and that response contains new access token
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.refresh_url,
            data={"refresh": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Valid refresh jwt endpoint did not return 200 OK",
        )
        self.assertRegex(
            response.data["access"],
            expected_regex=self.jwt_regexp,
            msg="Valid refresh jwt endpoint returned jwt did not match reg exp",
        )


class LogoutAuthEndpointTest(BaseAuthTestSetup):
    def test_redis_read_write(self):
        """
        Test reading and writing to redis db
        """
        tmp = "test_redis_key"
        result = cache.set(key=tmp, value="test_key_value", timeout=3000)
        logger.debug(f"Result writing to redis {result}")
        self.assertEqual(result, True)
        reading = cache.has_key(tmp)
        logger.debug(f"Result exists in redis {reading}")
        self.assertEqual(reading, True)
        cache.delete(tmp)

    def test_protected_endpoint_after_logout(self):
        """
        Test if a user that is logged out cannot use protected endpoints with
        the same tokens
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.logout_url,
            data={"access": creds["access"], "refresh": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(
            self.logout_url,
            data={"access": creds["access"], "refresh": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg="A protected endpoint was accessed after logout",
        )

    def test_logout_view(self):
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.logout_url,
            data={"access": creds["access"], "refresh": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_only_for_authorized(self):
        """
        An authorized request must include Authorization header with JWT
        """
        creds = self.get_logged_in_tokens(self.username_user_1)
        response = self.client.post(
            self.logout_url,
            data={"access": creds["access"], "refresh": creds["refresh"]},
            # headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginAuthEndpointTest(BaseAuthTestSetup):
    def test_valid_user_login(self):
        response = self.client.post(
            self.login_url,
            {"username": self.username_user_1, "password": self.password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")
        self.assertContains(response, "refresh")

    def test_invalid_credentials_rejected(self):
        response = self.client.post(
            self.login_url, {"username": "not_exists", "password": "not_exists"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegistrarionAuthEndpointTest(BaseAuthTestSetup):
    def test_valid_user_registration(self):
        "Valid test case"
        response = self.client.post(
            self.register_url,
            {
                "username": "unique234",
                "email": "unique_mail@gmail.com",
                "password": self.password,
            },
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_register_unique_email(self):
        "Email must be unique"
        response = self.client.post(
            self.register_url,
            {
                "username": "unique_name23472938",
                "email": "not_so_unique@gmail.com",
                "password": self.password,
            },
        )
        response = self.client.post(
            self.register_url,
            {
                "username": "unique_123322938",
                "email": "not_so_unique@gmail.com",
                "password": self.password,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_unique_username(self):
        "Username must be unique"
        response = self.client.post(
            self.register_url,
            {
                "username": "unique_1231238",
                "email": "not_so_unique123@gmail.com",
                "password": self.password,
            },
        )
        response = self.client.post(
            self.register_url,
            {
                "username": "unique_1231238",
                "email": "not_so_uniqu34324e123@gmail.com",
                "password": self.password,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
