from django.test import TestCase
from ..models import User, Account, BaseCategory, UserCategory
from rest_framework.test import APIClient
from django_redis import get_redis_connection


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.login_url = "/api/auth/login"
        cls.logout_url = "/api/auth/logout"
        cls.register_url = "/api/auth/register"
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

        cls.redis_conn = get_redis_connection("default")

        return super().setUpTestData()

    def login_user(self, username, password="1234"):
        """Set up methods for retreiving a logged-in user"""
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

    def login_admin(self):
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

    def tearDown(self):
        self.redis_conn.flushdb()
