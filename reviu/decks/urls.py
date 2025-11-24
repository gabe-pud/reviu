from django.urls import path
from . import views



urlpatterns = [
    path('decks/', views.decks_view, name='decks'),
]

