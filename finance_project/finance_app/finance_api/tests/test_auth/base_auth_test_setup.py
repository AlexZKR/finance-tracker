from typing import Dict

from ..base_test_setup import BaseTestSetup


class BaseAuthTestSetup(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.jwt_regexp = r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)"

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
