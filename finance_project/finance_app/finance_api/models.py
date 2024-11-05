from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

from .models_choices import (
    CURRENCY_CHOICES,
    COLOR_CHOICES,
    CATEGORY_CHOICES,
    TRANSACTION_TYPES,
)


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.email} - {self.username}"


class Account(models.Model):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="BYN")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    display_color = models.CharField(
        max_length=7, choices=COLOR_CHOICES, default="#4CAF50"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.user}"


class BaseCategory(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    base_category = models.ForeignKey(
        BaseCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    display_color = models.CharField(
        max_length=7, choices=COLOR_CHOICES, default="#4CAF50"
    )

    def clean(self):
        if UserCategory.objects.filter(
            user=self.user,
            base_category=self.base_category,
            custom_name=self.custom_name,
        ):
            raise ValidationError("UserCategory must be unique!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.custom_name if self.custom_name else self.base_category.name


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        UserCategory, on_delete=models.SET_DEFAULT, default="null_category", blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction")

    transaction_type = models.CharField(
        choices=TRANSACTION_TYPES, max_length=2, default="EX"
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account} - {self.transaction_type} - {self.amount}"


class AccountBudget(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="account_budgets"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="budgets"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} - AccBudg for {self.account.name}: {self.amount}"


class CategoryBudget(models.Model):
    """
    Budget for category (i.e. Category: Food; )
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="category_budgets"
    )
    user_category = models.ForeignKey(
        UserCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    base_category = models.ForeignKey(
        BaseCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def clean(self):
        """
        Custom model validation rules
        """
        if self.base_category and self.user_category:
            raise ValidationError(
                "Only one of base_category or user_category should be set."
            )
        if not self.base_category and not self.user_category:
            raise ValidationError("One of base_category or user_category must be set.")
        if self.start_date > self.end_date:
            raise ValidationError("Start date can't be earlier than end date")
        if self.start_date < date.today():
            raise ValidationError("Start date can't be earlier than today")
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        category_name = (
            self.user_category.custom_name
            if self.user_category
            else self.base_category.name
        )
        return f"{self.user} - Budget for {category_name}: {self.amount}"
