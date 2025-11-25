from django.shortcuts import render,redirect
import requests
from datetime import date, datetime

# Create your views here.
def main_page(request):
    hoje = date.today()

    if request.session.get('auth_token') == None:
        return redirect('login')

    headers={
        "Authorization":request.session.get('auth_token')
    }

    try:
        response = requests.get('http://localhost:8080/decks',headers=headers)
        response.raise_for_status() 
        dados_api = response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'decks': []}

    decks_brutos = dados_api
    
    decks_processados = []
    cards_a_revisar_total = 0

    for deck in decks_brutos:
        total_cards = len(deck.get('cards', []))
        cards_a_revisar_hoje = 0

        for card in deck.get('cards', []):
            data_revisao_str = card.get('nextReview')
            
            if data_revisao_str:
                try:
                    data_revisao = datetime.strptime(data_revisao_str, '%Y-%m-%d').date()

                    if data_revisao <= hoje:
                        cards_a_revisar_hoje += 1
                        cards_a_revisar_total += 1
                        
                except ValueError:
                    print(f"Aviso: Data de revisão inválida para o card {card.get('id')}.")
                    pass

        deck_simplificado = {
            'id':deck['id'],
            'name': deck['name'],
            'quantidade_cards': total_cards,
            'cards_a_revisar': cards_a_revisar_hoje,
        }
        
        decks_processados.append(deck_simplificado)

    context = {
        'username': request.session.get('name'),
        'cards_a_revisar': cards_a_revisar_total,
        'decks': decks_processados
    }

    return render(request, 'main_page/index.html', context)