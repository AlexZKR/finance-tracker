from ..base_test_setup import BaseTestSetup
from ...models import Account


class BaseAccountTestSetup(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.test_account_user_1 = Account.objects.create(
            user=self.test_user_1, name="test_acc", amount=1000
        )
        self.test_account_user_2 = Account.objects.create(
            user=self.test_user_2, name="test_acc_2", amount=1000
        )
