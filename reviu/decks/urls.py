from django.urls import path
from . import views



urlpatterns = [
    path('decks/', views.decks_view, name='decks'),
    path('card-review/', views.card_review, name='card-review'),
]

