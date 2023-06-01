from rest_framework.permissions import BasePermission

from users.models import User, UserRoles


class IsOwner(BasePermission):
    message = 'Нет доступа к подборке!!'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsAdOwner(BasePermission):
    message = 'Нет доступа к объявлению! Вы не являетесь его владельцем!'

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsStaff(BasePermission):
    message = 'Вы не являетесь админом либо модератором'

    def has_permission(self, request, view):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]
