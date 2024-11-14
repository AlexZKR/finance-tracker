import logging
from typing import Dict

from django.test import TestCase
from ..models import User, Account, BaseCategory, UserCategory
from rest_framework.test import APIClient

logger = logging.getLogger("__name__")


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.login_url = "/api/auth/login"
        cls.logout_url = "/api/auth/logout"
        cls.register_url = "/api/auth/register"
        cls.refresh_url = "/api/auth/refresh"
        cls.verify_url = "/api/auth/verify"

        cls.accounts_list_url = "/api/accounts"

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

        cls.test_account_user_1 = Account.objects.create(
            user=cls.test_user_1, name="test_acc", amount=1000
        )
        cls.test_account_user_2 = Account.objects.create(
            user=cls.test_user_2, name="test_acc_2", amount=1000
        )

        cls.test_base_category = BaseCategory.objects.create(name="groceries")
        cls.custom_name = "custom name"

        cls.base_category = BaseCategory.objects.create(name="test_base_cat")
        cls.user_category = UserCategory.objects.create(
            user=cls.test_user_1,
            base_category=cls.base_category,
            custom_name="test_custom_cat",
        )

        cls.jwt_regexp = r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)"
        return super().setUpTestData()

    def get_logged_out_tokens(self, username, password="1234") -> Dict[str, str]:
        """
        Logins in and loggins out a test user
        for retreiving a logged-out user tokens.

        """
        response = self.client.post(
            self.login_url,
            {"username": username, "password": password},
        )
        response_data = response.json()
        self.client.post(
            self.logout_url,
            {"access": response_data["access"], "refresh": response_data["refresh"]},
            headers={"Authorization": f"Bearer {response_data["access"]}"},
        )
        return {
            "Authorization_header": f"Bearer {response_data["access"]}",
            "access": response_data["access"],
            "refresh": response_data["refresh"],
        }

    def get_logged_in_tokens(self, username, password="1234") -> Dict[str, str]:
        """Logins in a test user for retreiving logged-in user tokens"""
        response = self.client.post(
            self.login_url,
            {"username": username, "password": password},
        )
        response_data = response.json()
        return {
            "Authorization_header": f"Bearer {response_data["access"]}",
            "access": response_data["access"],
            "refresh": response_data["refresh"],
        }

    def get_logged_in_admin_tokens(self) -> Dict[str, str]:
        """Set up methods for retreiving a logged-in admin"""

        response = self.client.post(
            self.login_url,
            {
                "username": self.username_admin,
                "password": self.password,
            },
        )
        response_data = response.json()
        return {
            "Authorization_header": f"Bearer {response_data["access"]}",
            "access": response_data["access"],
            "refresh": response_data["refresh"],
        }
