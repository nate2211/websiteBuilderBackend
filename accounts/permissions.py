from rest_framework.permissions import BasePermission

class IsImageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming the AccountImage model has an 'account' attribute
        return obj.account == request.user
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming the AccountImage model has an 'account' attribute
        return obj == request.user