from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Access to objects (accounts, transaction, categories) of a user
    has only this user and admins
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
