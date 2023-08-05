from django.http import Http404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import exceptions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS', 'VIEW')


class DjangoModelPermissionsFull(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.list_%(model_name)s'],
        'VIEW': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
                not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)

    def get_required_object_permissions(self, method, model_cls):
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            return True
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        perms = self.get_required_object_permissions('VIEW', model_cls)
        if not user.has_perms(perms):
            if request.method in SAFE_METHODS:
                raise Http404
            read_perms = self.get_required_object_permissions('VIEW', model_cls)
            if not user.has_perms(read_perms, obj):
                raise Http404
            return False
        return True
