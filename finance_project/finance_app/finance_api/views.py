from .models import Account, Transaction, User
from .serializers import (
    AccountHyperlinkedSerializer,
    TransactionHyperlinkedSerializer,
    UserHyperlinkedSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "accounts": reverse("account-list", request=request, format=format),
        }
    )


class TransactionDetailed(APIView):
    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        account = transaction.account.get()
        user = transaction.user.get()
        serializer_context = {
            "request": request,
        }
        serializer = TransactionHyperlinkedSerializer(
            transaction,
            account,
            user,
            context=serializer_context,
        )


class TransactionList(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer_context = {
            "request": request,
        }
        serilizer = TransactionHyperlinkedSerializer(
            transactions, many=True, context=serializer_context
        )
        return Response(serilizer.data)


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer_context = {
            "request": request,
        }
        serializer = UserHyperlinkedSerializer(
            users, many=True, context=serializer_context
        )
        return Response(serializer.data)


class UserDetailed(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        serializer_context = {
            "request": request,
        }
        serializer = UserHyperlinkedSerializer(
            user,
            context=serializer_context,
        )
        return Response(serializer.data)


class AccountList(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer_context = {
            "request": request,
        }
        serializer = AccountHyperlinkedSerializer(
            accounts, many=True, context=serializer_context
        )
        return Response(serializer.data)


class AccountDetailed(APIView):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer_context = {
            "request": request,
        }
        serializer = AccountHyperlinkedSerializer(
            account,
            context=serializer_context,
        )
        return Response(serializer.data)
