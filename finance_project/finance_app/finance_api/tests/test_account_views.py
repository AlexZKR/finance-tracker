from rest_framework import status
from .base_test_setup import BaseTestSetup
from ..models import Account


class AccountViewsTest(BaseTestSetup):
    def setUp(self):
        self.test_account_user_1 = Account.objects.create(
            user=self.test_user_1, name="test_acc", amount=1000
        )
        self.test_account_user_2 = Account.objects.create(
            user=self.test_user_2, name="test_acc_2", amount=1000
        )

    def test_user_can_update_valid_account(self):
        """
        Assert that user can update an account with valid data
        """
        user_1_cred = super().get_logged_in_tokens(username=self.username_user_1)
        response = self.client.get(
            path=f"{self.accounts_list_url}/{self.test_account_user_1.id}",
            headers={"Authorization": user_1_cred["Authorization_header"]},
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Valid post request for account creation did not return 201 Created ",
        )

    def test_user_can_update_valid_account(self):
        """
        Assert that user can create an account with valid data
        """
        user_1_cred = super().get_logged_in_tokens(username=self.username_user_1)
        response = self.client.post(
            path=f"{self.accounts_list_url}",
            data={
                "name": "new_test_account",
                "amount": 1000,
            },
            headers={"Authorization": user_1_cred["Authorization_header"]},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Valid post request for account creation did not return 201 Created ",
        )

    def test_user_cant_retreive_others_account(self):
        "Ensure that user can't retreive the account of other user by id"
        user_1_cred = super().get_logged_in_tokens(username=self.username_user_1)
        response = self.client.get(
            path=f"{self.accounts_list_url}/{self.test_account_user_2.id}",
            headers={"Authorization": user_1_cred["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_retreive_his_account(self):
        "Ensure that user can retreive his account details by id"
        user_cred = super().get_logged_in_tokens(username=self.username_user_1)
        response = self.client.get(
            path=f"{self.accounts_list_url}/{self.test_account_user_1.id}",
            headers={"Authorization": user_cred["Authorization_header"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["id"], self.test_account_user_1.id)

    def test_admin_can_retreive_any_account(self):
        "Ensure that only admin can get any account by id"
        admin_cred = super().get_logged_in_admin_tokens()
        test_account_id = self.test_account_user_1.id
        response = self.client.get(
            path=f"{self.accounts_list_url}/{test_account_id}",
            headers={"Authorization": admin_cred["Authorization_header"]},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Account list endpoint did not return 200 OK \
            after admin tried to get ususal user's account by id",
        )

    def test_retrieve_account_list_for_usual_authorized_user(self):
        "Ensure that auth-ed user gets his account list"
        creds = super().get_logged_in_tokens(username=self.username_user_1)
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
