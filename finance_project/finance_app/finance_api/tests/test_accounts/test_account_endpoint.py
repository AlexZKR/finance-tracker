import logging
from .base_account_test_setup import BaseAccountTestSetup
from rest_framework import status

logger = logging.getLogger("__name__")


class AccountViewsTest(BaseAccountTestSetup):
    def test_user_can_delete_his_account(self):
        """
        Assert that user can delete [DELETE] his account
        """
        response = self.client.delete(
            path=f"{self.accounts_url}/{self.test_account_user_1.id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg="Valid delete request did not return 204 NO CONTENT",
        )

    def test_user_cant_update_account_with_invalid_data(self):
        """
        Assert that user can't update [PUT or PATCH] an account with invalid data
        """
        response = self.client.put(
            path=f"{self.accounts_url}/{self.test_account_user_1.id}",
            headers=self.get_auth_header(username=self.username_user_1),
            content_type="application/json",
            data={
                "name": self.test_account_user_1.name,
                "currency": self.test_account_user_1.currency,
                "amount": -10,
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="PUT request with invalid data did not return 400 BAD REQUEST",
        )

    def test_user_can_partially_update_valid_account(self):
        """
        Assert that user can partially update [PATCH] an account with valid data
        """
        response = self.client.get(
            path=f"{self.accounts_url}/{self.test_account_user_1.id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        account_id = response.data.get("id")
        old_name = response.data.get("name")
        response = self.client.patch(
            path=f"{self.accounts_url}/{account_id}",
            headers=self.get_auth_header(username=self.username_user_1),
            content_type="application/json",
            data={
                "name": "new_name",
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Valid put request for account partial update did not return 200 OK",
        )
        response = self.client.get(
            path=f"{self.accounts_url}/{account_id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        new_name = response.data.get("name")
        self.assertNotEqual(
            old_name,
            new_name,
            msg=f"Valid patch request for account partial update did not partially update account's name from {old_name} to {new_name}",
        )

    def test_user_can_update_valid_account(self):
        """
        Assert that user can update [PUT] an account with valid data
        """
        response = self.client.get(
            path=f"{self.accounts_url}/{self.test_account_user_1.id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        account_id = response.data.get("id")
        old_name = response.data.get("name")
        response = self.client.put(
            path=f"{self.accounts_url}/{account_id}",
            headers=self.get_auth_header(username=self.username_user_1),
            content_type="application/json",
            data={
                "name": "new_name",
                "currency": self.test_account_user_1.currency,
                "amount": self.test_account_user_1.amount,
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Valid put request for account update did not return 200 OK",
        )
        response = self.client.get(
            path=f"{self.accounts_url}/{account_id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        new_name = response.data.get("name")
        self.assertNotEqual(
            old_name,
            new_name,
            msg=f"Valid put request for account update did not update account's name from {old_name} to {new_name}",
        )

    def test_user_cant_create_invalid_account(self):
        """
        Assert that user can't create an account with invalid data
        """
        response = self.client.post(
            path=f"{self.accounts_url}",
            data={
                "name": "new_test_account",
                "amount": -123421,
            },
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="POST request with invalid data for account creation did not return 400 BAD REQUEST ",
        )

    def test_user_can_create_valid_account(self):
        """
        Assert that user can create an account with valid data
        """
        response = self.client.post(
            path=f"{self.accounts_url}",
            data={
                "name": "new_test_account",
                "amount": 1000,
            },
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Valid post request for account creation did not return 201 Created ",
        )

    def test_user_cant_retreive_others_account(self):
        "Ensure that user can't retreive the account of other user by id"
        response = self.client.get(
            path=f"{self.accounts_url}/{self.test_account_user_2.id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_retreive_his_account(self):
        "Ensure that user can retreive his account details by id"
        response = self.client.get(
            path=f"{self.accounts_url}/{self.test_account_user_1.id}",
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["id"], self.test_account_user_1.id)

    def test_admin_can_retreive_any_account(self):
        "Ensure that only admin can get any account by id"
        test_account_id = self.test_account_user_1.id
        response = self.client.get(
            path=f"{self.accounts_url}/{test_account_id}",
            headers=self.get_auth_header(username=self.username_admin, admin=True),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Account list endpoint did not return 200 OK \
            after admin tried to get ususal user's account by id",
        )

    def test_retrieve_account_list_for_usual_authorized_user(self):
        "Ensure that auth-ed user gets his account list"
        response = self.client.get(
            path=self.accounts_url,
            headers=self.get_auth_header(username=self.username_user_1),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_account_list_for_usual_non_authorized_user(self):
        "Ensure that non auth-ed user can't get accounts and app handles this properly"
        response = self.client.get(
            path=self.accounts_url,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
