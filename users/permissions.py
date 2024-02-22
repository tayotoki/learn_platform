from django.apps import apps
from rest_framework import permissions


class IsOwnerOrManager(permissions.BasePermission):
    """
    Permission для доступа к контенту или профилю пользователя
    """

    PROHIBITED_FOR_MANAGERS = ("DELETE", "POST")

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method not in permissions.SAFE_METHODS + self.PROHIBITED_FOR_MANAGERS:
            if obj._meta.app_label == apps.get_containing_app_config("courses").label:  # noqa
                return (
                    obj.author == request.user
                    or request.user.groups.filter(name="managers").exists()
                )
            if obj._meta.app_label == apps.get_containing_app_config("users").label:  # noqa
                return obj == request.user or request.user.groups.filter(name="managers").exists()

        if request.method in self.PROHIBITED_FOR_MANAGERS + permissions.SAFE_METHODS:
            return (
                user == request.user if (user := getattr(obj, "author", None)) else obj == request.user
            )

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in self.PROHIBITED_FOR_MANAGERS:
            return not request.user.groups.filter(name="managers").exists()

        return True
