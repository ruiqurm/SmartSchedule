from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """

    Allows access only to
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return bool(obj.user == request.user)
