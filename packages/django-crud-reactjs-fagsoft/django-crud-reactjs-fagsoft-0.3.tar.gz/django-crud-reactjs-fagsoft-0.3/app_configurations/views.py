from rest_framework import viewsets
from rest_framework.response import Response
from utils.permissions.permissions_utilities import DjangoModelPermissionsFull
from rest_framework.exceptions import ValidationError
from .serializers import GeneralInfoConfigurationSerializer
from .models import GeneralInfoConfiguration


class AppConfiguracionViewSet(viewsets.ViewSet):
    def list(self, request):
        from .services import create_update_general_info
        general_info_configuration = GeneralInfoConfiguration.objects
        general_info_configuration = general_info_configuration.first() if general_info_configuration.exists() else create_update_general_info()
        return Response({
            "general_info_configuration": GeneralInfoConfigurationSerializer(general_info_configuration,
                                                                             context={'request': request}).data,
        })


class AppGeneralInfoConfigurationViewSet(AppConfiguracionViewSet, viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsFull]
    queryset = GeneralInfoConfiguration.objects.all()
    serializer_class = GeneralInfoConfigurationSerializer

    def create(self, request, *args, **kwargs):
        raise ValidationError({'_error': 'Metodo crear no disponible'})

    def destroy(self, request, *args, **kwargs):
        raise ValidationError({'_error': 'Metodo eliminar no disponible'})

    def list(self, request):
        return super().list(request)
