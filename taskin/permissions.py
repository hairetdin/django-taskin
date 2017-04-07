from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

from .models import Project


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    only read object allow authenticated user
    """

    def has_permission(self, request, view):
        #allow all to superuser
        if request.user.is_superuser:
            return True

        return (
            request.method in permissions.SAFE_METHODS and
            request.user and
            request.user.is_authenticated
        )


class IsMember(permissions.BasePermission):
    """
    check the user right for current_project
    """

    def has_object_permission(self, request, view, obj):

        current_project = obj

        try:
            current_project_member = current_project.projectmember_set.filter(user=request.user).last()
        except ObjectDoesNotExist:
            current_project_member = None

        if request.user.is_superuser:
            return True

        if current_project_member:
            if (current_project_member.is_project_admin() or
                current_project_member.is_project_executor()):
                return True

            if (request.method in permissions.SAFE_METHODS and
                current_project_member.is_project_watcher()):
                return True

        return False


class IsProjectMember(permissions.BasePermission):
    """
    check the user right for current_project
    """

    def has_object_permission(self, request, view, obj):

        current_project = obj.project

        try:
            current_project_member = current_project.projectmember_set.filter(user=request.user).last()
        except ObjectDoesNotExist:
            current_project_member = None

        if request.user.is_superuser:
            return True

        if current_project_member:
            if (current_project_member.is_project_admin() or
                current_project_member.is_project_executor()):
                return True

            if (request.method in permissions.SAFE_METHODS and
                current_project_member.is_project_watcher()):
                return True

        return False


class IsExecutorProjectMember(permissions.BasePermission):
    """
    check the user right for current_project
    """

    def has_object_permission(self, request, view, obj):

        current_project = obj.task.project

        try:
            current_project_member = current_project.projectmember_set.get(user=request.user)
        except ObjectDoesNotExist:
            current_project_member = None

        if request.user.is_superuser:
            return True

        if current_project_member:
            if (current_project_member.is_project_admin() or
                current_project_member.is_project_executor()):
                return True

            if (request.method in permissions.SAFE_METHODS and
                current_project_member.is_project_watcher()):
                return True

        return False
