from .base_account_test_setup import BaseAccountTestSetup
from ...serializers import AccountSerializer
from rest_framework import serializers


class AccountSerializerTest(BaseAccountTestSetup):
    def test_amount_must_be_greate_than_zero(self):
        """
        Assert that `AccountSerializer` raises `ValidationError` when supplied with
        amount < 0
        """
        with self.assertRaises(
            serializers.ValidationError,
            msg="Account serializer did not raise ValidationError after suplied with amount < 0",
        ):
            serializer = AccountSerializer(
                data={
                    "name": "test",
                    "amount": -10,
                }
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.test_user_1)

    def test_valid_model_passes(self):
        """
        Assert that `AccountSerializer` validates correct data
        """
        try:
            serializer = AccountSerializer(
                data={
                    "name": "test",
                    "amount": 1000,
                }
            )
            if serializer.is_valid():
                serializer.save(user=self.test_user_1)
            else:
                self.fail(
                    f"Serializer did not validate correct data: {serializer.errors}"
                )
        except Exception as e:
            self.fail(f"Valid model serializer validaton failed with exception: {e}")
