from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.conf import settings

from ..models import *

def get_seed_type(session):
    steps = session.steps.all()
    element_ids = steps.values_list('_visited_element', flat=True)
    elements_names = VoiceServiceElement.objects.filter(id__in=element_ids).values_list('name', flat=True)
    for seed_type in SeedOffer.SEED_TYPES_CHOICES:
        if elements_names.filter(name__istartswith=seed_type[1]):
            return seed_type[0]

# up to 99 (incl.)
def get_label_names_from_value(value):
    label_names = []
    str_value = str(value)
    if value < 20 or value % 10 == 0:
        label_names.append(str_value)
    else:
        list_str_value = list(str_value)
        if list_str_value[1] != 0:
            second = list_str_value[1]
            list_str_value[1] = '0'
            label_names.append(''.join(list_str_value))
            label_names.append(second)
        else:
            label_names.append(str_value)
    return label_names

def get_voice_url_by_name(name, language):
    return VoiceLabel.objects.filter(name__iexact=name).first().get_voice_fragment_url(language)

def create_get_offer_context(seed_offers, offer_i, session, session_id):
    seed_offer = seed_offers[offer_i]

    if offer_i + 1 >= len(seed_offers):
        next_offer_i = 0
    else:
        next_offer_i = offer_i + 1

    if offer_i - 1 < 0:
        prev_offer_i = len(seed_offers) - 1
    else:
        prev_offer_i = offer_i - 1
    
    caller_id = seed_offer.telephone_number

    audio = []
    for label_name in get_label_names_from_value(seed_offer.amount_of_seeds):
        audio.append(get_voice_url_by_name(label_name, session.language))
    audio.append(get_voice_url_by_name('bags_of', session.language))
    audio.append(get_voice_url_by_name(seed_offer.seed_name(), session.language))
    audio.append(get_voice_url_by_name('for', session.language))
    for label_name in get_label_names_from_value(seed_offer.seeds_price):
        audio.append(get_voice_url_by_name(label_name, session.language))
    audio.append(get_voice_url_by_name('per_bag_in', session.language))
    audio.append(settings.MEDIA_URL + str(seed_offer.location.audio))

    return {
        'next_offer_i': next_offer_i,
        'prev_offer_i': prev_offer_i,
        'caller_id': caller_id,
        'offer_audio': audio,
        'session_id': session_id
    }


def get_offer(request, offer_i, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    seed_type = get_seed_type(session)
    seed_offers = [obj for obj in SeedOffer.objects.filter(seed_type=seed_type) if obj.days_to_go() < 0]
    seed_offers.sort(key=lambda x: x.created_at)
    return render(request, 'offer.xml', create_get_offer_context(seed_offers, offer_i, session, session_id), content_type='text/xml')


def get_offer_no_offer(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    seed_type = get_seed_type(session)
    seed_offers = [obj for obj in SeedOffer.objects.filter(seed_type=seed_type) if obj.days_to_go() < 0]
    seed_offers.sort(key=lambda x: x.created_at)
    return render(request, 'offer.xml', create_get_offer_context(seed_offers, 0, session, session_id), content_type='text/xml')






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

def transfer(request, telephone_number):
    context = {
        'telephone_number': telephone_number
    }

    return render(request, 'transfer.xml',context, content_type='text/xml')