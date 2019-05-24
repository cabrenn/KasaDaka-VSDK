from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from ..models import SeedOffer

class OffersView(generic.ListView):
    template_name = 'offers.html'
    context_object_name = 'farmers_offers'


    def get_queryset(self):
        seed_offers = [obj for obj in SeedOffer.objects.all() if obj.days_to_go() < 0]
        seed_offers.sort(key=lambda x: x.days_to_go())
        return seed_offers