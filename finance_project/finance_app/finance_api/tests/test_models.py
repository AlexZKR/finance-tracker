from django.test import TestCase
from ..models import BaseCategory, UserCategory, User
from rest_framework.test import APIClient
from rest_framework import status


class UserCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testUser", password="password")
        self.test_base_category = BaseCategory.objects.create(name="groceries")
        self.custom_name = "custom name"

    def test_create_user_category_with_base_category(self):
        """
        Creation of a predefined category
        """
        user_category = UserCategory.objects.create(
            user=self.user, base_category=self.test_base_category
        )
        self.assertEqual(user_category.base_category, self.test_base_category)
        self.assertIsNone(user_category.custom_name)

    def test_create_custom_user_category(self):
        """
        Creation of a custom category unique for a user
        """
        user_category = UserCategory.objects.create(
            user=self.user, custom_name=self.custom_name
        )

        self.assertEqual(user_category.custom_name, self.custom_name)
        self.assertIsNone(user_category.base_category)

    def test_unique_category_constraint_for_base_category(self):
        """
        Test that two predefined categories cannot be assigned to one user
        """
        UserCategory.objects.create(
            user=self.user, base_category=self.test_base_category
        )

        with self.assertRaises(Exception):
            UserCategory.objects.create(
                user=self.user, base_category=self.test_base_category
            )

    def test_unique_category_constraint_for_custom_category(self):
        """
        Test that two custom categories cannot be assigned to one user
        """
        UserCategory.objects.create(user=self.user, custom_name=self.custom_name)

        with self.assertRaises(Exception):
            UserCategory.objects.create(user=self.user, custom_name=self.custom_name)

    def test_base_category_cant_have_custom_name(self):
        """
        Test that if a category is predefined it can't have a custom name which approrpiate only for custom user-defined categories
        """
        with self.assertRaises(Exception):
            UserCategory.objects.create(
                user=self.user,
                custom_name=self.custom_name,
                baseCategory=self.test_base_category,
            )


class CategoryBudgetModelTest(TestCase):
    pass
