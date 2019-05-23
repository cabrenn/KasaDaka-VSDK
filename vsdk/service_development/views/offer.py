from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def get_seed_type(session):
    steps = session.steps.all()
    element_ids = steps.values_list('_visited_element', flat=True)
    elements_names = VoiceServiceElement.objects.filter(id__in=element_ids).values_list('name', flat=True)
    for seed_type in SeedOffer.SEED_TYPES_CHOICES:
        if elements_names.filter(name__istartswith=seed_type[1]):
            return seed_type[0]


def save_offer(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)

    #print(session.session_dtmf_set.all())
    o = SeedOffer()
    o.seed_type = get_seed_type(session)
    o.seeds_price = session.session_dtmf.filter(category__name = 'seed_price').first().value
    o.amount_of_seeds = session.session_dtmf.filter(category__name = 'seed_amount').first().value
    o.days_online = session.session_dtmf.filter(category__name = 'seed_available').first().value
    o.telephone_number = session.caller_id
    o.location = session.session.filter(category__name = 'seed_location').first() 
    o.save()
    return redirect(request.POST['redirect'])
