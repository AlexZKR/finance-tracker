from .base_auth_test_setup import BaseAuthTestSetup
from ...models import User


class UserModelTest(BaseAuthTestSetup):
    def test_valid_model_passes(self):
        try:
            User.objects.create_user(
                email="unique@gmail.com",
                username="unique_name",
                password=self.password,
            )
        except Exception as e:
            self.fail(f"Valid model creation failed with exception: {e}")

    def test_email_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="unique_email_1@gmail.com",
                username="unique_user_12311",
                password=self.password,
            )
            User.objects.create_user(
                email="unique_email_1@gmail.com",
                username="unique_user_223",
                password=self.password,
            )

    def test_username_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="unique_email_22321@gmail.com",
                username="unique_user_1",
                password=self.password,
            )
            User.objects.create_user(
                email="unique_email_312312@gmail.com",
                username="unique_user_1",
                password=self.password,
            )
