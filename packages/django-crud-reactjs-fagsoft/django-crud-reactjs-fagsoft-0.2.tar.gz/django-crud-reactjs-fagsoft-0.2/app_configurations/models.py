import random

from django.db import models
from pilkit.processors import ResizeToFit
from imagekit.models import ProcessedImageField, ImageSpecField


class GeneralInfoConfiguration(models.Model):
    application_name = models.CharField(max_length=50, default='App. Name')

    def imagen_logo_upload_to(self, filename) -> str:  # pragma: no cover
        random_number = random.randint(11111, 99999)
        return "img/logo/%s01j%sj10%s.%s" % (self.id, random_number, self.id, filename.split('.')[-1])

    logo = ProcessedImageField(
        processors=[
            ResizeToFit(height=500, width=500, upscale=False),
        ],
        format='PNG',
        options={'quality': 100},
        null=True,
        blank=True,
        upload_to=imagen_logo_upload_to
    )

    icon_small = ImageSpecField(
        source='logo',
        processors=[
            ResizeToFit(height=32, width=32, upscale=False),
        ],
        format='PNG'
    )

    icon_medium = ImageSpecField(
        source='logo',
        processors=[
            ResizeToFit(height=48, width=48, upscale=False),
        ],
        format='PNG'
    )

    logo_small = ImageSpecField(
        source='logo',
        processors=[
            ResizeToFit(height=256, width=256, upscale=False),
        ],
        format='PNG'
    )

    logo_medium = ImageSpecField(
        source='logo',
        processors=[
            ResizeToFit(height=300, width=300, upscale=False),
        ],
        format='PNG'
    )
