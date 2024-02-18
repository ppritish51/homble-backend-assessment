from rest_framework import permissions


class IsSupervisor(permissions.BasePermission):
    """
    Custom permission to only allow members of the 'Supervisors' group to access a view.
    """

    def has_permission(self, request, view):
        # Check if the user is part of the 'Supervisors' group
        return request.user.groups.filter(name='Supervisors').exists()
