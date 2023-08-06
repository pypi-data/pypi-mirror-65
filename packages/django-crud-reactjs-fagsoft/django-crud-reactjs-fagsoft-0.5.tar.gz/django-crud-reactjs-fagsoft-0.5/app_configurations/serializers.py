from rest_framework import serializers
from .models import GeneralInfoConfiguration


class GeneralInfoConfigurationSerializer(serializers.ModelSerializer):
    icon_small = serializers.ImageField(read_only=True)
    icon_medium = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)
    favicon_medium = serializers.ImageField(read_only=True)
    favicon_small = serializers.ImageField(read_only=True)

    def update(self, instance, validated_data):
        logo = validated_data.get('logo', None)
        favicon = validated_data.get('favicon', None)
        application_name = validated_data.get('application_name', None)

        address = validated_data.get('address', None)
        contact_emails = validated_data.get('contact_emails', None)
        attention_schedule = validated_data.get('attention_schedule', None)
        facebook = validated_data.get('facebook', None)
        whatsaap = validated_data.get('whatsaap', None)
        instagram = validated_data.get('instagram', None)
        linkedin = validated_data.get('linkedin', None)
        youtube = validated_data.get('youtube', None)
        twitter = validated_data.get('twitter', None)

        from .services import create_update_general_info
        configuracion = create_update_general_info(
            logo=logo,
            application_name=application_name,
            favicon=favicon,
            twitter=twitter,
            youtube=youtube,
            linkedin=linkedin,
            instagram=instagram,
            whatsaap=whatsaap,
            facebook=facebook,
            attention_schedule=attention_schedule,
            contact_emails=contact_emails,
            address=address
        )
        return configuracion

    class Meta:
        model = GeneralInfoConfiguration
        fields = [
            'id',
            'logo',
            'application_name',
            'address',
            'contact_emails',
            'attention_schedule',
            'facebook',
            'whatsaap',
            'instagram',
            'linkedin',
            'youtube',
            'twitter',
            'icon_small',
            'icon_medium',
            'logo_small',
            'logo_medium',
            'favicon',
            'favicon_medium',
            'favicon_small',
        ]
