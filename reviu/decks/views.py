from django.shortcuts import render, redirect
import requests
from datetime import datetime, timedelta, date
import json

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

    context = {
        "decks":decks,
        "current_deck_id": current_deck_id,
        "current_deck_name": current_deck_name,
        "cards":cards
    }
    return render(request, 'decks/deck.html', context)


def criar_deck(request):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
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

    return redirect("decks")


def deletar_deck(request,deck_id):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
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

    return redirect("decks")


def criar_card(request, deck_id):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
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

    return redirect("decks")


def alterar_card(request, deck_id, card_id):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
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

    return redirect("decks")


def deletar_card(request, deck_id, card_id):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
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
        
    return redirect("decks")


def gerar_cards_from_file(request, deck_id):
    """Upload a PDF to the external API to generate cards, then bulk-create them.

    Expects a POST with a file in `request.FILES['file']` and will:
    1. POST the file to /decks/{deck_id}/cards/generate-from-file with form field `file` and `type=pdf`.
    2. POST the returned cards to /decks/{deck_id}/cards/bulk as JSON to create them.
    """
    if request.session.get('auth_token') is None:
        return redirect('login')

    if request.method != 'POST':
        return redirect('decks')

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return redirect('decks')

    API_BASE = 'http://localhost:8080'
    headers = {}
    token = request.session.get('auth_token')
    if token:
        headers['Authorization'] = token

    # 1) Send the file to the generate-from-file endpoint
    gen_url = f"{API_BASE}/decks/{deck_id}/cards/generate-from-file"
    files = {
        'file': (uploaded_file.name, uploaded_file.read(), 'application/pdf')
    }
    data = {'type': 'pdf'}

    try:
        resp = requests.post(gen_url, headers=headers, files=files, data=data, timeout=120)
        resp.raise_for_status()
        gen_result = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar arquivo para gerar cards: {e}")
        return redirect('decks')

    # Normalize cards list from response
    if isinstance(gen_result, dict) and 'cards' in gen_result:
        cards_list = gen_result.get('cards') or []
    elif isinstance(gen_result, list):
        cards_list = gen_result
    else:
        # Unexpected shape
        cards_list = []

    if not cards_list:
        return redirect('decks')

    # 2) Send the generated cards in bulk to create them
    bulk_url = f"{API_BASE}/decks/{deck_id}/cards/bulk"
    try:
        # include Authorization header and let requests set Content-Type
        resp2 = requests.post(bulk_url, headers=headers, json={'cards': cards_list}, timeout=60)
        resp2.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar cards em bulk: {e}")

    return redirect('decks')


def card_review(request, deck_id):
    if request.session.get('auth_token') is None:
        return redirect('login')

    API_BASE = 'http://localhost:8080'
    headers = {}
    token = request.session.get('auth_token')
    if token:
        headers['Authorization'] = token

    try:
        if request.method == 'POST':
            card_id = request.POST.get('card_id')
            evaluation = request.POST.get('evaluation') or request.POST.get('rating')

            payload = {}
            if evaluation is not None:
                payload['evaluation'] = evaluation

            review_url = f"{API_BASE}/decks/{deck_id}/cards/{card_id}/review"
            try:
                resp = requests.post(review_url, headers=headers, json=payload, timeout=10)
                resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Erro ao enviar review para API: {e}")

            return redirect('card_review', deck_id=deck_id)

        due_url = f"{API_BASE}/decks/{deck_id}/cards/due"
        try:
            resp = requests.get(due_url, headers=headers, timeout=10)
            resp.raise_for_status()
            cards_api = resp.json() or []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar cards pendentes da API: {e}")
            cards_api = []

        next_card = None
        if isinstance(cards_api, list) and len(cards_api) > 0:
            i = cards_api[0]
            next_card = {
                'id': i.get('id'),
                'frontText': i.get('frontText'),
                'backText': i.get('backText'),
                'imageUrl': i.get('imageUrl'),
                'audioUrl': i.get('audioUrl'),
                'raw': i,
            }

        return render(request, 'card-review/card-review.html', {
            'card': next_card,
            'deck_id': deck_id,
        })

    except Exception as e:
        print(f"Erro inesperado em card_review: {e}")
        return render(request, 'card-review/card-review.html', {
            'card': None,
            'deck_id': deck_id,
            'error': 'Erro ao comunicar com o serviço de revisão.'
        })
