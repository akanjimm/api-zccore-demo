
from django.urls import path
from .views import EventCreateView, event_list_view, EventUpdateView

urlpatterns = [
    path('', event_list_view),
    path('create/', EventCreateView.as_view()),
    path('update/<str:data_id>/', EventUpdateView.as_view()),
    ]
