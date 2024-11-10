from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase


class UserViewsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_email_1 = "test_email_1@gmail.com"
        self.test_email_2 = "test_email_2@gmail.com"
        self.test_user_name_1 = "test_username_1"
        self.test_user_name_2 = "test_username_2"
        self.test_password = "jfUFh81387_018!"

    def test_valid_user_registration(self):
        "Valid test case"
        response = self.client.post(
            "/api/users/register",
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
            "/api/users/register",
            {
                "username": self.test_user_name_1,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        response = self.client.post(
            "/api/users/register",
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
            "/api/users/register",
            {
                "username": self.test_user_name_1,
                "email": self.test_email_1,
                "password": self.test_password,
            },
        )
        response = self.client.post(
            "/api/users/register",
            {
                "username": self.test_user_name_1,
                "email": self.test_email_2,
                "password": self.test_password,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
