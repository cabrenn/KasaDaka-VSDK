from django.urls import path

from . import views

app_name= 'service-development-web'
urlpatterns = [
    path('', views.OffersView.as_view(), name='offers'),
]

