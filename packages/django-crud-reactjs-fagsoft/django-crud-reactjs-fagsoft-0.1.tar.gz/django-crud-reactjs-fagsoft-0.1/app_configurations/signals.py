from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch import receiver

from .models import GeneralInfoConfiguration


@receiver(pre_delete, sender=GeneralInfoConfiguration)
def logo_pre_delete(sender, instance, **kwargs):
    instance.logo.delete(False)


@receiver(post_init, sender=GeneralInfoConfiguration)
def backup_logo_path(sender, instance, **kwargs):
    instance._current_logo = instance.logo


@receiver(post_save, sender=GeneralInfoConfiguration)
def delete_logo(sender, instance, **kwargs):
    if hasattr(instance, '_current_logo'):
        if instance._current_logo != instance.logo:
            instance._current_logo.delete(save=False)
