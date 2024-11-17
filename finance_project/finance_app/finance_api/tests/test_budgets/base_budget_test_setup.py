from ..base_test_setup import BaseTestSetup
from ...models import BaseCategory, UserCategory


class BaseBudgetTestSetup(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.base_category = BaseCategory.objects.create(name="test_base_cat")
        self.user_category = UserCategory.objects.create(
            user=self.test_user_1,
            base_category=self.base_category,
            custom_name="test_custom_cat",
        )
