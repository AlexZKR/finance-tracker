import logging
from .base_test_setup import BaseTestSetup
from rest_framework import status
from django.core.cache import cache


logger = logging.getLogger("__name__")


class RefreshAPITest(BaseTestSetup):
    """
    Test refresh tokens logic
    """

    def test_access_cant_be_used_for_refreshing(self):
        """
        Assert that access token cant be used for refreshing
        """
        creds = self.login_user(self.username_user_1)
        response = self.client.post(
            self.refresh_url,
            data={"refresh": creds["access"]},  # sending access instead of refresh
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()  # Parse JSON content
        self.assertIn("Token has wrong type", response_data.get("detail", ""))

    def test_refresh_is_authenticated_only(self):
        """
        Assert that refresh endpoint is restricted only for authenticated users
        """
        creds = self.login_user(self.username_user_1)
        response = self.client.post(
            self.refresh_url,
            data={"refresh": creds["access"]},  # not providing auth header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_refresh_case(self):
        """
        Assert that user can refresh his access token using refresh token
        and that response contains new access token
        """
        creds = self.login_user(self.username_user_1)
        response = self.client.post(
            self.refresh_url,
            data={"refresh": creds["refresh"]},
            headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(
            response.data["access"],
            expected_regex=r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)",
        )


class LogoutAPITest(BaseTestSetup):
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

    def test_double_logout(self):
        """
        Test if a user that is logged out cannot use protected endpoints with
        the same tokens
        """
        creds = self.login_user(self.username_user_1)
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_view(self):
        creds = self.login_user(self.username_user_1)
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
        creds = self.login_user(self.username_user_1)
        response = self.client.post(
            self.logout_url,
            data={"access": creds["access"], "refresh": creds["refresh"]},
            # headers={"Authorization": f"Bearer {creds["access"]}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginAPITest(BaseTestSetup):
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


class RegistrarionAPITest(BaseTestSetup):
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
