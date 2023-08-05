from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ExtendedUser


class UserSerializer(serializers.ModelSerializer):
    to_string = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()
    security_pin = serializers.CharField(source='extended_user.security_pin', allow_null=True, required=False)
    security_qr = serializers.CharField(source='extended_user.security_qr', allow_null=True, required=False)
    gender = serializers.CharField(source='extended_user.gender', allow_null=True, required=False)
    date_of_birth = serializers.DateField(
        source='extended_user.date_of_birth', format="%Y-%m-%d",
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ', 'iso-8601']
    )

    def get_profile_image_url(self, obj):  # pragma: no cover
        return obj.extended_user.profile_image.url if hasattr(
            obj,
            'extended_user'
        ) and obj.extended_user.profile_image else None

    def get_to_string(self, instance):  # pragma: no cover
        return ('%s %s' % (instance.first_name, instance.last_name)).title()

    def update(self, instance, validated_data):
        extended_user = validated_data.pop('extended_user') if 'extended_user' in validated_data else None
        user = super().update(instance, validated_data)
        if extended_user is not None:
            security_pin = extended_user.get('security_pin', None)
            security_qr = extended_user.get('security_qr', None)
            gender = extended_user.get('gender', None)
            date_of_birth = extended_user.get('date_of_birth', None)
            if hasattr(user, 'extended_user'):
                extended_user = user.extended_user
            else:
                extended_user = ExtendedUser.objects.create(user_id=instance.id)
            extended_user.security_pin = security_pin
            extended_user.security_qr = security_qr
            extended_user.gender = gender
            extended_user.date_of_birth = date_of_birth
            extended_user.save()
        return user

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'password',
            'username',
            'last_login',
            'date_joined',
            'is_superuser',
            'groups',
            'user_permissions',
            'to_string',
            'profile_image_url',
            'security_pin',
            'security_qr',
            'gender',
            'date_of_birth',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        extended_user = validated_data.pop('extended_user') if 'extended_user' in validated_data else None
        validated_data.pop('groups', None)
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if extended_user is not None:
            security_pin = extended_user.get('security_pin', None)
            security_qr = extended_user.get('security_qr', None)
            gender = extended_user.get('gender', None)
            date_of_birth = extended_user.get('date_of_birth', None)
            extended_user = ExtendedUser.objects.create(user_id=user.id)
            extended_user.security_pin = security_pin
            extended_user.security_qr = security_qr
            extended_user.gender = gender
            extended_user.date_of_birth = date_of_birth
            extended_user.save()
        return user


class UserWithDetailSerializer(UserSerializer):
    pass


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({'_error': 'El usuario y la contraseña no coinciden con ningún usuario!'})
