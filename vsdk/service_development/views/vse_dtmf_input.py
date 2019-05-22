from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def record_get_redirect_url(record_element, session):
    return record_element.redirect.get_absolute_url(session)

def record_generate_context(record_element, session):
    language = get_object_or_404(Language, pk=2) # session.language
    redirect_url = record_get_redirect_url(record_element, session)


    voice_label = record_element.voice_label.get_voice_fragment_url(language)
    # ask_confirmation_voice_label = record_element.ask_confirmation_voice_label.get_voice_fragment_url(language)
    # repeat_voice_label = record_element.repeat_voice_label.get_voice_fragment_url(language)
    # final_voice_label = record_element.final_voice_label.get_voice_fragment_url(language)
    # did_not_hear_voice_label = record_element.not_heard_voice_label.get_voice_fragment_url(language)
    # max_time_input = record_element.max_time_input


    context = {'record': record_element,
               'redirect_url': redirect_url,
               'dtmf_input_voice_label' : voice_label,
               }

    return context


def dtmf_input_view(request, element_id, session_id):
    dtmf_input_element = get_object_or_404(DtmfInput, pk=element_id)
    voice_service = dtmf_input_element.service
    session = lookup_or_create_session(voice_service, session_id)


    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        result = DtmfUserInput()

        result.session = session
        result.value = int(request.POST['dtmf_input_entered'])
        result.category = dtmf_input_element.input_category 

        result.save()

        #if record_element.map_to_call_session_property in vars(session).keys():
        #    setattr(session, record_element.map_to_call_session_property, value)

        # redirect to next element
        return redirect(request.POST['redirect'])

    session.record_step(dtmf_input_element)
    context = record_generate_context(dtmf_input_element, session)

    context['url'] = request.get_full_path(False)

    return render(request, 'dtmf_input.xml', context, content_type='text/xml')