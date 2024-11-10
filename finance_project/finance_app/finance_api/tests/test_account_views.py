from rest_framework import status
from .base_test_setup import BaseTestSetup


class AccountViewsTest(BaseTestSetup):
    

    def test_user_cant_retreive_others_account(self):
        "Ensure that user can't retreive the account of other user by id"
        user_1_cred = super().login_user(username=self.username_user_1)
        response = self.client.get(
            path=f"{self.accounts_list_url}/{self.test_account_user_2.id}",
            headers={"Authorization": user_1_cred["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_retreive_his_account(self):
        "Ensure that user can retreive his account details by id"
        user_cred = super().login_user(username=self.username_user_1)
        response = self.client.get(
            path=f"{self.accounts_list_url}/{self.test_account_user_1.id}",
            headers={"Authorization": user_cred["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["id"], self.test_account_user_1.id)

    def test_admin_can_retreive_any_account(self):
        "Ensure that only admin can get any account by id"
        admin_cred = super().login_admin()
        response = self.client.get(
            path=f"{self.accounts_list_url}/1",
            headers={"Authorization": admin_cred["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_account_list_for_usual_authorized_user(self):
        "Ensure that auth-ed user gets his account list"
        creds = super().login_user(username=self.username_user_1)
        response = self.client.get(
            path=self.accounts_list_url,
            headers={"Authorization": creds["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_account_list_for_usual_non_authorized_user(self):
        "Ensure that non auth-ed user can't get accounts and app handles this properly"
        response = self.client.get(
            path=self.accounts_list_url,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
