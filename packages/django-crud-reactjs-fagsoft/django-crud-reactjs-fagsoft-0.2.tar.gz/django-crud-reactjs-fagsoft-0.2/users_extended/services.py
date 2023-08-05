from django.contrib.auth.models import User, Permission, Group
from knox.models import AuthToken
from rest_framework import serializers


def user_get_token(
        user_id: int
) -> str:
    user = User.objects.get(pk=user_id)
    tokens = AuthToken.objects.filter(user=user)
    tokens.delete()
    _, token = AuthToken.objects.create(user)
    return token


def user_exist_username(
        username: str
) -> bool:
    if username and User.objects.filter(username=username).exists():
        return True
    return False


def user_change_password(
        user_id: int,
        password_old: str,
        password_new: str,
        password_new_confirmation: str
) -> User:
    user = User.objects.get(pk=user_id)
    if not user.check_password(password_old):
        raise serializers.ValidationError({'_error': 'La contraseña suministrada no coincide con el user'})
    if not password_new == password_new_confirmation:
        raise serializers.ValidationError({'_error': 'La contraseña nueva con su confirmación no coincide'})
    user.set_password(password_new)
    user.save()
    return user


def user_add_permission(
        permission_id: int,
        user_id: int
) -> User:
    user = User.objects.get(pk=user_id)
    permission = Permission.objects.get(id=permission_id)
    has_group = user.user_permissions.filter(id=permission_id).exists()
    if not has_group:
        user.user_permissions.add(permission)
    else:
        user.user_permissions.remove(permission)
    return user


def user_add_group(
        grupo_id: int,
        user_id: int
) -> User:
    user = User.objects.get(pk=user_id)
    group = Group.objects.get(id=grupo_id)

    has_group = user.groups.filter(id=grupo_id).exists()
    if not has_group:
        user.groups.add(group)
    else:
        user.groups.remove(group)
    return user
