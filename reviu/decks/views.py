from django.shortcuts import render

# Create your views here.

def decks_view(request):
    return render(request, 'decks/deck.html')
