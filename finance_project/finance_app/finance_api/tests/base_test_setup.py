import logging


from django.test import TestCase
from ..models import User
from rest_framework.test import APIClient

logger = logging.getLogger("__name__")


class BaseTestSetup(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()

        cls.login_url = "/api/auth/login"
        cls.logout_url = "/api/auth/logout"
        cls.register_url = "/api/auth/register"
        cls.refresh_url = "/api/auth/refresh"
        cls.verify_url = "/api/auth/verify"

        cls.accounts_url = "/api/accounts"

        cls.username_user_1 = "testuser1"
        cls.username_user_2 = "testuser2"
        cls.username_admin = "test_admin1"

        cls.password = "1234"

        cls.test_email_user_1 = "test_email_1_@gmail.com"
        cls.test_email_user_2 = "test_email_2_@gmail.com"
        cls.admin_test_email = "test_admin1@gmail.com"

        cls.test_user_1 = User.objects.create_user(
            username=cls.username_user_1,
            email=cls.test_email_user_1,
            password=cls.password,
        )
        cls.test_user_2 = User.objects.create_user(
            username=cls.username_user_2,
            email=cls.test_email_user_2,
            password=cls.password,
        )
        cls.test_admin = User.objects.create_superuser(
            username=cls.username_admin,
            email=cls.admin_test_email,
            password=cls.password,
        )

    def get_auth_header(self, username, password="1234", admin=False) -> str:
        """Logins in a test user for retreiving valid authentication header"""
        if admin:
            username = self.username_admin
        response = self.client.post(
            self.login_url,
            {"username": username, "password": password},
        )
        response_data = response.json()
        return {"Authorization": f"Bearer {response_data["access"]}"}
