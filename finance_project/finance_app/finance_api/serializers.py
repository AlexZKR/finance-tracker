from rest_framework import serializers
from .models import User, Account, Transaction, Budget, Category


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "category",
            "user",
            "transaction_type",
            "date",
            "description",
            "amount",
        ]


class AccountSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Transaction.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "currency",
            "amount",
            "display_color",
            "user",
            "transactions",
        ]


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ["name", "user", "display_color"]


class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Budget
        fields = [
            "budget_type",
            "amount",
            "start_date",
            "end_date",
            "user",
            "account",
            "category",
        ]


class UserSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)
    categories = CategorySerializer(many=True)
    budgets = BudgetSerializer(many=True)

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
