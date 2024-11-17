from .base_category_test_setup import BaseCategoryTestSetup
from ...models import UserCategory


class UserCategoryModelTest(BaseCategoryTestSetup):
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
            UserCategory.objects.create(
                user=self.test_user_1, custom_name=self.custom_name
            )

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
