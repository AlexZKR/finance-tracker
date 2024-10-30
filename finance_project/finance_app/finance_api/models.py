from django.db import models
from django.contrib.auth.models import AbstractUser

from .models_choices import (
    CURRENCY_CHOICES,
    COLOR_CHOICES,
    CATEGORY_CHOICES,
    TRANSACTION_TYPES,
    BUDGET_TYPES,
)


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


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


class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_color = models.CharField(
        max_length=7, choices=COLOR_CHOICES, default="#4CAF50"
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default="null_category", blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPES, max_length=2, default="EX"
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account} - {self.transaction_type} - {self.amount}"


class Budget(models.Model):
    budget_type = models.CharField(choices=BUDGET_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.budget_type} - {self.amount}"
