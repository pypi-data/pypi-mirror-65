from rest_framework import serializers
from .models import GeneralInfoConfiguration


class GeneralInfoConfigurationSerializer(serializers.ModelSerializer):
    icon_small = serializers.ImageField(read_only=True)
    icon_medium = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)

    def update(self, instance, validated_data):
        logo = validated_data.get('logo', None)
        application_name = validated_data.get('application_name', None)
        from .services import create_update_general_info
        configuracion = create_update_general_info(logo=logo, application_name=application_name)
        return configuracion

    class Meta:
        model = GeneralInfoConfiguration
        fields = [
            'id',
            'logo',
            'application_name',
            'icon_small',
            'icon_medium',
            'logo_small',
            'logo_medium',
        ]
