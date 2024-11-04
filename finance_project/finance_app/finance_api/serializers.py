from rest_framework import serializers
from .models import (
    AccountBudget,
    CategoryBudget,
    User,
    Account,
    Transaction,
    UserCategory,
)


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "account_id",
            "category_id",
            "user_id",
            "transaction_type",
            "date",
            "description",
            "amount",
        ]


class AccountSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Transaction.objects.all()
    )
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "user_id",
            "name",
            "currency",
            "amount",
            "display_color",
            "transactions",
        ]


class CategorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserCategory
        fields = ["name", "user_id", "display_color"]


class AccountBudgetSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AccountBudget
        fields = [
            "id",
            "user_id",
            "account_id",
            "amount",
            "start_date",
            "end_date",
        ]


class CategoryBudgetSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    base_category_id = serializers.PrimaryKeyRelatedField(
        allow_null=True, read_only=True
    )
    user_category_id = serializers.PrimaryKeyRelatedField(
        allow_null=True, read_only=True
    )

    class Meta:
        model = CategoryBudget
        fields = [
            "id",
            "user_id",
            "base_category_id",
            "user_category_id",
            "amount",
            "start_date",
            "end_date",
        ]


class UserSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)
    categories = CategorySerializer(many=True)
    account_budgets = AccountBudgetSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "accounts",
            "categories",
            "budgets",
        ]
