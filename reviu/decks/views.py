from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta, date
import json

# Create your views here.


def _safe_json(response):
    """Safely parse JSON from a requests.Response, returning {} on empty body or parse error."""
    if response is None:
        return {}
    try:
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()
    except ValueError:
        return {}


def _format_next_review(next_review_raw, today=None):
    """Format a nextReview date string (YYYY-MM-DD) into the desired display form.

    Returns 'hoje' if date is today or in the past, 'amanhã' if it's tomorrow,
    otherwise returns 'MM-DD'. If parsing fails or value is falsy, returns
    the original value or empty string.
    """
    if not next_review_raw:
        return ''
    try:
        next_date = datetime.strptime(next_review_raw, '%Y-%m-%d').date()
    except Exception:
        return next_review_raw

    if today is None:
        today = date.today()

    if next_date <= today:
        return 'hoje'
    if next_date == today + timedelta(days=1):
        return 'amanhã'
    return next_date.strftime('%m-%d')

def decks_view(request):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
    headers={
        "Authorization":request.session.get('auth_token')
    }

    try:
        response = requests.get('http://localhost:8080/decks',headers=headers)
        response.raise_for_status()
        dados_api = _safe_json(response)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'decks': []}
    
    decks = []
    current_deck_id = request.POST.get("current_deck_id")
    current_deck_name = ""

    if dados_api != {'decks': []}:
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
            dados_api = _safe_json(response)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar decks da API: {e}")
            dados_api = {'cards': []}
        
        cards = []

        for i in dados_api:
            formatted_next = _format_next_review(i.get("nextReview"), hoje)

            card = {
                "id": i.get("id"),
                "frontText": i.get("frontText"),
                "backText": i.get("backText"),
                "nextReview": formatted_next,
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
        dados_api = _safe_json(response)

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
        dados_api = _safe_json(response)

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
    # Build payload from POST values. If files are used, the external API
    # should accept multipart; this view forwards JSON when non-file.
    data = {
        "frontText": request.POST.get("frontText"),
        "backText": request.POST.get("backText"),
    }

    try:
        # If files are present, forward them as multipart/form-data
        if request.FILES and len(request.FILES) > 0:
            files = {}
            # forward any file fields that the template might send
            for name, f in request.FILES.items():
                files[name] = (f.name, f.read(), getattr(f, 'content_type', 'application/octet-stream'))
            resp = requests.post(url, headers=headers, files=files, data=data)
        else:
            resp = requests.post(url, headers=headers, json=data)

        resp.raise_for_status()
        created = _safe_json(resp)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar card na API: {e}")
        # If AJAX, return JSON error so front-end can show it
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'api_error', 'message': str(e)}, status=500)
        return redirect('decks')

    # If AJAX request, return created card JSON so client can insert it in DOM
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # format nextReview for client display (keep other fields untouched)
        if isinstance(created, dict) and 'nextReview' in created:
            created['nextReview'] = _format_next_review(created.get('nextReview'))
        # resp.status_code may be 201 or 200; return that status where possible
        try:
            status = resp.status_code
        except Exception:
            status = 200
        return JsonResponse(created, safe=False, status=status)

    return redirect('decks')


def alterar_card(request, deck_id, card_id):
    if request.session.get('auth_token') == None:
        return redirect('login')
    
    url = "http://localhost:8080/decks/"+str(deck_id)+"/cards/"+str(card_id)

    headers={
        "Authorization":request.session.get('auth_token')
    }
    # Build payload from POST values. If files are used, forward as multipart.
    data = {
        "frontText": request.POST.get("frontText"),
        "backText": request.POST.get("backText")
    }

    try:
        if request.FILES and len(request.FILES) > 0:
            files = {}
            for name, f in request.FILES.items():
                files[name] = (f.name, f.read(), getattr(f, 'content_type', 'application/octet-stream'))
            resp = requests.put(url, headers=headers, files=files, data=data)
        else:
            resp = requests.put(url, headers=headers, json=data)

        resp.raise_for_status()
        updated = _safe_json(resp)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao alterar card na API: {e}")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'api_error', 'message': str(e)}, status=500)
        return redirect('decks')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # ensure nextReview is formatted for client display
        if isinstance(updated, dict) and 'nextReview' in updated:
            updated['nextReview'] = _format_next_review(updated.get('nextReview'))
        try:
            status = resp.status_code
        except Exception:
            status = 200
        return JsonResponse(updated, safe=False, status=status)

    return redirect('decks')


def deletar_card(request, deck_id, card_id):
    if request.session.get('auth_token') == None:
        # If AJAX request, return JSON error so front-end can handle it
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'not_authenticated'}, status=401)
        return redirect('login')
    
    url = "http://localhost:8080/decks/"+str(deck_id)+"/cards/"+str(card_id)

    headers={
        "Authorization":request.session.get('auth_token')
    }

    try:
        response = requests.delete(url,headers=headers)
        response.raise_for_status()
        dados_api = _safe_json(response)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar decks da API: {e}")
        dados_api = {'cards': []}
        # If AJAX, return JSON error so front-end can show an error
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'api_error', 'message': str(e)}, status=500)
        
    # If this is an AJAX request, return a minimal JSON success response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    
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
        # For AJAX clients, return a JSON error; otherwise redirect.
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'method_not_allowed'}, status=405)
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
        gen_result = _safe_json(resp)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar arquivo para gerar cards: {e}")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'api_upload_failed', 'message': str(e)}, status=502)
        return redirect('decks')

    # Normalize cards list from response
    # Some backends may return the JSON payload as a string (e.g. '"[... ]"').
    # If we got a string, try to parse it into Python objects first.
    if isinstance(gen_result, str):
        try:
            parsed = json.loads(gen_result)
            gen_result = parsed
        except Exception:
            # leave gen_result as-is; fallback logic below will handle unexpected shapes
            pass

    if isinstance(gen_result, dict) and 'cards' in gen_result:
        cards_list = gen_result.get('cards') or []
    elif isinstance(gen_result, list):
        cards_list = gen_result
    else:
        # Unexpected shape
        cards_list = []

    if not cards_list:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'no_cards_generated'}, status=204)
        return redirect('decks')

    # 2) Send the generated cards in bulk to create them
    # The API bulk endpoint expects a JSON array (List) in the request body.
    bulk_url = f"{API_BASE}/decks/{deck_id}/cards/bulk"
    try:
        # send the raw list as the JSON body (not wrapped in an object)
        resp2 = requests.post(bulk_url, headers=headers, json=cards_list, timeout=60)
        resp2.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar cards em bulk: {e}")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'bulk_create_failed', 'message': str(e)}, status=502)
        return redirect('decks')

    # Success — if this was an AJAX request, return JSON with details so the
    # client can update the UI without a full reload.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'created': len(cards_list)}, status=201)

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
            cards_api = _safe_json(resp) or []
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
