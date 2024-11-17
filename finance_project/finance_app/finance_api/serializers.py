from rest_framework import serializers
from .models import (
    AccountBudget,
    BaseCategory,
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
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    transactions = serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, read_only=True
    )

    def validate_amount(self, value):
        """
        Check that amount is greater than 0
        """
        if value < 0:
            raise serializers.ValidationError("Amount must be greater than zero!")
        return value

    class Meta:
        model = Account
        fields = [
            "id",
            "user_id",
            "name",
            "currency",
            "amount",
            "transactions",
        ]


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCategory
        fields = ["id", "name"]


class UserCategorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    base_category_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserCategory
        fields = [
            "id",
            "user_id",
            "custom_name",
            "base_category_id",
        ]


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
    accounts = AccountSerializer(many=True, required=False)
    categories = UserCategorySerializer(many=True, required=False)
    account_budgets = AccountBudgetSerializer(many=True, required=False)

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
            "account_budgets",
        ]
