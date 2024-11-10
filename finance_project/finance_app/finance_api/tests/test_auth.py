from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase


class LoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login"
        self.register_url = "/api/auth/register"

        self.username = "test_user"
        self.password = "12334fhf_edhD"
        self.test_email = "test_email@gmail.com"

        self.test_user = self.client.post(
            self.register_url,
            {
                "username": self.username,
                "email": self.test_email,
                "password": self.password,
            },
        )

    def login_user(self):
        response = self.client.post(
            self.login_url, {"username": self.username, "password": self.password}
        )
        return {"access": response["access"], "refresh": response["refresh"]}

    
    
    def test_valid_user_login(self):
        response = self.client.post(
            self.login_url, {"username": self.username, "password": self.password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")
        self.assertContains(response, "refresh")

    def test_invalid_credentials_rejected(self):
        response = self.client.post(
            self.login_url, {"username": "not_exists", "password": "not_exists"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegistrarionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register"

        self.test_email_1 = "test_email_1@gmail.com"
        self.test_email_2 = "test_email_2@gmail.com"
        self.test_user_name_1 = "test_username_1"
        self.test_user_name_2 = "test_username_2"
        self.test_password = "jfUFh81387_018!"

    def test_valid_user_registration(self):
        "Valid test case"
        response = self.client.post(
            self.register_url,
            {
                "username": self.test_user_name_1,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_register_unique_email(self):
        "Email must be unique"
        response = self.client.post(
            self.register_url,
            {
                "username": self.test_user_name_1,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        response = self.client.post(
            self.register_url,
            {
                "username": self.test_user_name_2,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_unique_username(self):
        "Username must be unique"
        response = self.client.post(
            self.register_url,
            {
                "username": self.test_user_name_1,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        response = self.client.post(
            self.register_url,
            {
                "username": self.test_user_name_1,
                "email": self.test_email_2,
                "password": self.test_password,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
