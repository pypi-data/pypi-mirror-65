from django.contrib.auth.models import Permission, Group
from rest_framework import serializers

from utils.serializers.serializers_utilities import CustomSerializerMixin
from .models import PermissionPlus


class PermissionSerializer(CustomSerializerMixin, serializers.ModelSerializer):
    name_plus = serializers.CharField(source='plus.name', allow_null=True, allow_blank=True)
    active = serializers.BooleanField(source='plus.active')
    to_string = serializers.SerializerMethodField()
    content_type_label = serializers.CharField(source='content_type.app_label', read_only=True)
    content_type_model = serializers.CharField(source='content_type.app_label', read_only=True)

    def get_to_string(self, instance):  # pragma: no cover
        return instance.plus.name.title() if hasattr(
            instance,
            'plus'
        ) and instance.plus.name else instance.name.title()

    class Meta:
        model = Permission
        fields = [
            'id',
            'to_string',
            'codename',
            'content_type',
            'content_type_label',
            'content_type_model',
            'name',
            'name_plus',
            'active',
        ]

    def update(self, instance, validated_data):
        plus_data = validated_data.pop('plus', None)

        if hasattr(instance, 'plus'):
            plus = instance.plus
        else:
            plus = PermissionPlus.objects.create(**plus_data)

        for attr, value in plus_data.items():
            setattr(plus, attr, value)
        plus.permission = instance
        plus.save()
        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    to_string = serializers.SerializerMethodField()

    def get_to_string(self, instance):  # pragma: no cover
        return instance.name.title()

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
            'to_string'
        ]
