from datetime import timedelta
from datetime import date

from .base_budget_test_setup import BaseBudgetTestSetup
from ...models import CategoryBudget
from django.core.exceptions import ValidationError


class CategoryBudgetModelTest(BaseBudgetTestSetup):
    def setUp(self):
        super().setUp()
        self.today = date.today()
        self.tomorrow = date.today() + timedelta(days=1)
        self.yesterday = date.today() - timedelta(days=1)

    def test_valid_object_passes(self):
        try:
            CategoryBudget.objects.create(
                user=self.test_user_1,
                user_category=self.user_category,
                amount=100,
                start_date=self.today,
                end_date=self.tomorrow,
            )
        except Exception as e:
            self.fail(f"Valid object creation failed with exception {e}")

    def test_only_base_or_user_cat_is_set(self):
        with self.assertRaises(ValidationError):
            CategoryBudget.objects.create(
                user=self.test_user_1,
                user_category=self.user_category,
                base_category=self.base_category,
            )

    def test_either_base_or_user_cat_is_set(self):
        with self.assertRaises(ValidationError):
            CategoryBudget.objects.create(
                user=self.test_user_1,
            )

    def test_start_date_is_later_than_end_date(self):
        with self.assertRaises(ValidationError):
            CategoryBudget.objects.create(
                user=self.test_user_1,
                base_category=self.base_category,
                start_date=date.today(),
                end_date=self.yesterday,
                amount=100,
            )

    def test_start_date_is_today_or_later(self):
        with self.assertRaises(ValidationError):
            CategoryBudget.objects.create(
                user=self.test_user_1,
                base_category=self.base_category,
                start_date=self.yesterday,
                end_date=self.tomorrow,
                amount=100,
            )

    def test_amount_is_greater_that_zero(self):
        with self.assertRaises(ValidationError):
            CategoryBudget.objects.create(
                user=self.test_user_1,
                base_category=self.base_category,
                start_date=self.today,
                end_date=self.tomorrow,
                amount=-1,
            )
