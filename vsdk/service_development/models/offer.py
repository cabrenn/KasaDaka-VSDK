from django.db import models

from .user_input import SpokenUserInput, DtmfUserInput
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

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
    
    telephone_number = models.CharField(max_length=100)

    def seed_name(self):
        for seed_choice in self.SEED_TYPES_CHOICES:
            if self.seed_type in seed_choice:
                return seed_choice[1]