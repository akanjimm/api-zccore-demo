from django.urls import path

from .views import EventCreateView

urlpatterns = [
    path('create/', EventCreateView.as_view()),
    ]