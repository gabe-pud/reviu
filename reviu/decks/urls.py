from django.urls import path
from . import views



urlpatterns = [
    path('decks/', views.decks_view, name='decks'),
    path('decks/crate', views.criar_deck, name="criar_deck"),
    path('decks/<int:deck_id>/delete/',views.deletar_deck, name="criar_deck"),
    path('decks/<int:deck_id>/cards/',  views.criar_card, name="criar_card"),
    path('decks/<int:deck_id>/cards/<int:card_id>/edit/', views.alterar_card, name="alterar_card"),
    path('decks/<int:deck_id>/cards/<int:card_id>/delete/', views.deletar_card, name="deletar_card"),
    path('card-review/', views.card_review, name='card-review'),
]

