from django.db import models
from django.contrib.auth.models import Permission


class PermissionPlus(models.Model):
    permission = models.OneToOneField(Permission, related_name='plus', null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(null=True, blank=True, max_length=200)
    active = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('list_permission', 'Can list permission'),
            ('list_group', 'Can list group'),
        )
