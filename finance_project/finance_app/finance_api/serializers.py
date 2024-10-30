from rest_framework import serializers
from .models import User, Account, Transaction, Budget, Category


class AccountHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    transactions = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail",  # Name of the URL pattern for the user detail view
        queryset=User.objects.all(),  # Ensure the queryset is provided
    )

    class Meta:
        model = Account
        fields = "__all__"

    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)

        # Add the email to the representation
        representation["user_email"] = instance.user.email if instance.user else None

        return representation


class UserHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    accounts = AccountHyperlinkedSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "url", "accounts"]


class TransactionHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"


class BudgetHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"


class CategoryHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
