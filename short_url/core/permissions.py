from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from .models import URL

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request:Request, view: View, obj:URL) -> bool:
        if view.action == "destroy":
            return request.user == obj.user or request.user.is_superuser
        return True