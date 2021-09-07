from django.urls import path

from .views import EventCreateView, event_list_view

urlpatterns = [
    path('', event_list_view),
    path('create/', EventCreateView.as_view()),
    ]