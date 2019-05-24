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
        seed_offers = [obj for obj in SeedOffer.objects.order_by('created_at') if obj.days_to_go() < 0]
        return seed_offers