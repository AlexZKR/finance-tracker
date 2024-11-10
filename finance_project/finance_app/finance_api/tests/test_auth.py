from .base_test_setup import BaseTestSetup
from rest_framework import status


class LoginAPITest(BaseTestSetup):
    def test_valid_user_login(self):
        response = self.client.post(
            self.login_url, {"username": self.username_user_1, "password": self.password}
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
