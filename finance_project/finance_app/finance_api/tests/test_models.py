from datetime import date, timedelta


from django.forms import ValidationError
from .base_test_setup import BaseTestSetup
from ..models import BaseCategory, Account, CategoryBudget, UserCategory, User
from ..models_choices import CURRENCY_CHOICES


class UserModelTest(BaseTestSetup):
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


class AccountModelTest(BaseTestSetup):
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


class UserCategoryModelTest(BaseTestSetup):
    def test_valid_model_passes(self):
        try:
            UserCategory.objects.create(
                user=self.test_user_1, base_category=self.test_base_category
            )
        except Exception as e:
            self.fail(f"Valid model creation failed with exception: {e}")

    def test_create_user_category_with_base_category(self):
        """
        Creation of a predefined category
        """
        user_category = UserCategory.objects.create(
            user=self.test_user_1, base_category=self.test_base_category
        )
        self.assertEqual(user_category.base_category, self.test_base_category)
        self.assertIsNone(user_category.custom_name)

    def test_create_custom_user_category(self):
        """
        Creation of a custom category unique for a user
        """
        user_category = UserCategory.objects.create(
            user=self.test_user_1, custom_name=self.custom_name
        )

        self.assertEqual(user_category.custom_name, self.custom_name)
        self.assertIsNone(user_category.base_category)

    def test_unique_category_constraint_for_base_category(self):
        """
        Test that two predefined categories cannot be assigned to one user
        """
        UserCategory.objects.create(
            user=self.test_user_1, base_category=self.test_base_category
        )

        with self.assertRaises(Exception):
            UserCategory.objects.create(
                user=self.test_user_1, base_category=self.test_base_category
            )

    def test_unique_category_constraint_for_custom_category(self):
        """
        Test that two custom categories cannot be assigned to one user
        """
        UserCategory.objects.create(user=self.test_user_1, custom_name=self.custom_name)

        with self.assertRaises(Exception):
            UserCategory.objects.create(user=self.test_user_1, custom_name=self.custom_name)

    def test_base_category_cant_have_custom_name(self):
        """
        Test that if a category is predefined it can't have a custom name which approrpiate only for custom user-defined categories
        """
        with self.assertRaises(Exception):
            UserCategory.objects.create(
                user=self.test_user_1,
                custom_name=self.custom_name,
                baseCategory=self.test_base_category,
            )


class CategoryBudgetModelTest(BaseTestSetup):
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
