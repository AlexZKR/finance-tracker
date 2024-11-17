from .base_account_test_setup import BaseAccountTestSetup
from ...models import Account, CURRENCY_CHOICES
from django.core.exceptions import ValidationError


class AccountModelTest(BaseAccountTestSetup):
    def test_valid_model_passes(self):
        try:
            Account.objects.create(
                user=self.test_user_1, currency=CURRENCY_CHOICES[0][0], amount=1000
            )
        except Exception as e:
            self.fail(f"Valid model creation failed with exception: {e}")

    def test_amount_greater_than_zero(self):
        with self.assertRaises(ValidationError):
            Account.objects.create(user=self.test_user_1, amount=-1)
