from django.conf.urls import url, include
from django.urls import path

from . import views

app_name= 'service-development'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^choice/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$', views.choice, name='choice'),
    url(r'^message/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$', views.message_presentation, name='message-presentation'),
    url(r'^start/(?P<voice_service_id>[0-9]+)$', views.voice_service_start, name='voice-service'),
    url(r'^start/(?P<voice_service_id>[0-9]+)/(?P<session_id>[0-9]+)$', views.voice_service_start, name='voice-service'),
    url(r'^user/register/(?P<session_id>[0-9]+)$', views.KasaDakaUserRegistration.as_view(), name = 'user-registration'),
    url(r'^language_select/(?P<session_id>[0-9]+)$', views.LanguageSelection.as_view(), name = 'language-selection'),
    url(r'^record/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$', views.record, name='record'),
    path('dtmfinput/<int:element_id>/<int:session_id>', views.dtmf_input_view, name='dtmfinput'),
    path('saveoffer/<int:session_id>', views.save_offer, name='saveoffer'),
    path('getoffer/<int:session_id>', views.get_offer_no_offer, name='getoffer'),
    path('getoffer/<int:offer_i>/<int:session_id>', views.get_offer, name='getoffer'),
    path('transfer/<str:telephone_number>', views.transfer, name='transfer'),
]

