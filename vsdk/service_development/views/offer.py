from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def save_offer(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    print(session.session_dtmf_set.all())

    return None
