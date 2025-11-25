from django.shortcuts import render, redirect
import requests
from datetime import datetime, timedelta, date

# Create your views here.

def decks_view(request):
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
    
    decks = []
    current_deck_id = request.POST.get("current_deck_id")
    current_deck_name = ""

    for i in dados_api:
        deck = {
            "id": i.get("id"),
            "name": i.get("name")
        }
        if request.POST.get("current_deck_id") is not None:
            if i.get("id") == int(request.POST.get("current_deck_id")):
                current_deck_name = i.get("name")
        decks.append(deck)
        
    
    if request.method == "POST":
        hoje = date.today()

        try:
            response = requests.get('http://localhost:8080/decks/'+current_deck_id+'/cards',headers=headers)
            response.raise_for_status()
            dados_api = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar decks da API: {e}")
            dados_api = {'cards': []}
        
        cards = []

        for i in dados_api:
            data_revisao = datetime.strptime(i.get("nextReview"), '%Y-%m-%d').date()
            if data_revisao <= hoje:
                data_revisao = "hoje"
            elif data_revisao == hoje + timedelta(days=1):
                data_revisao = "amanhã"
            else:
                data_revisao = data_revisao.strftime('%d/%m')
            
            card = {
                "id": i.get("id"),
                "frontText": i.get("frontText"),
                "backText": i.get("backText"),
                "nextReview": data_revisao,
                "imageUrl": i.get("imageUrl"),
                "audioUrl": i.get("audioUrl"),
            }
            cards.append(card)
    else:
        cards = []

    print(decks)
    context = {
        "decks":decks,
        "current_deck_id": current_deck_id,
        "current_deck_name": current_deck_name,
        "cards":cards
    }
    return render(request, 'decks/deck.html', context)


def criar_deck(request):
    headers={
        "Authorization":request.session.get('auth_token')
    }

    data = {
        "name": request.POST.get("name")
    }

    try:
        response = requests.post("http://localhost:8080/decks",headers=headers,json=data)
        response.raise_for_status()
        dados_api = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
    
    print(dados_api)

    return redirect("decks")


def deletar_deck(request,deck_id):
    url = "http://localhost:8080/decks/"+str(deck_id)

    headers={
        "Authorization":request.session.get('auth_token')
    }

    try:
        response = requests.delete(url,headers=headers)
        response.raise_for_status()
        dados_api = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
    
    print(dados_api)

    return redirect("decks")


def criar_card(request, deck_id):
    url = "http://localhost:8080/decks/"+str(deck_id)+"/cards"

    headers={
        "Authorization":request.session.get('auth_token')
    }

    data = {
        "frontText": request.POST.get("frontText"),
        "backText": request.POST.get("backText"),
    }

    try:
        response = requests.post(url,headers=headers,json=data)
        response.raise_for_status()
        dados_api = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
    
    print(dados_api)

    return redirect("decks")


def alterar_card(request, deck_id, card_id):
    url = "http://localhost:8080/decks/"+str(deck_id)+"/cards/"+str(card_id)

    headers={
        "Authorization":request.session.get('auth_token')
    }

    data = {
        "frontText": request.POST.get("frontText"),
        "backText": request.POST.get("backText")
    }

    try:
        response = requests.put(url,headers=headers,json=data)
        response.raise_for_status()
        dados_api = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
    
    print(dados_api)

    return redirect("decks")


def deletar_card(request, deck_id, card_id):
    url = "http://localhost:8080/decks/"+str(deck_id)+"/cards/"+str(card_id)

    headers={
        "Authorization":request.session.get('auth_token')
    }

    try:
        response = requests.delete(url,headers=headers)
        response.raise_for_status()
        dados_api = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
    
    print(dados_api)
    return redirect("decks")

