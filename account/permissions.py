from rest_framework.permissions import BasePermission


class IsAdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and (
                request.user.is_staff or (request.user.is_authenticated and hasattr(request.user, 'student')))


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser)


class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and (
                request.user.is_staff or (request.user.is_authenticated and hasattr(request.user, 'teacher')))


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'student')
