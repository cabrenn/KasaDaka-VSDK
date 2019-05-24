from django.db import models

from datetime import datetime

from .user_input import SpokenUserInput, DtmfUserInput
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from django.utils.safestring import mark_safe

from django.core.validators import MaxValueValidator, MinValueValidator


class SeedOffer(models.Model):
    RICE = 'RE'
    COTTON = 'CN'
    SORGHUM = 'SM'
    SEED_TYPES_CHOICES = (
        (RICE, 'Rice'),
        (COTTON, 'Cotton'),
        (SORGHUM, 'Sorghum'),
    )
    seed_type = models.CharField(
        max_length=2,
        choices=SEED_TYPES_CHOICES,
        default=RICE,
    )
    amount_of_seeds = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )
    seeds_price = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )
    days_online = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(90),
            MinValueValidator(1)
        ]
    )

    location = models.ForeignKey(
        SpokenUserInput,
        null=True,
        on_delete= models.SET_NULL,
        verbose_name =_('Offer location'),
        help_text = _("Recording of the offer's location")
    )
    audio = models.FileField(_('Audio'),
            blank=True,
            null=True,
            help_text = _("Audio File for web."))

    created_at = models.DateTimeField(default=datetime.now, blank=True)

    telephone_number = models.CharField(max_length=100)

    def days_to_go(self):
        return (datetime.now().replace(tzinfo=None) - self.created_at.replace(tzinfo=None)).days - self.days_online

    def seed_name(self):
        for seed_choice in self.SEED_TYPES_CHOICES:
            if self.seed_type in seed_choice:
                return seed_choice[1]

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = str('<audio src="%s" controls>'  % (file_url) + ugettext('Your browser does not support the audio element.') + '</audio>')
            return mark_safe(player_string)