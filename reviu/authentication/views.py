from django.shortcuts import render,redirect
import requests

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            senha = request.POST.get('password1')
        else:
            return redirect('register')

        data = {
            "name": request.POST.get('name'),
            "username": request.POST.get('name'),
            "email": request.POST.get('email'),
            "password": senha
        }

        info = requests.post('http://localhost:8080/auth/register', json=data)

        if info.status_code == 200 or info.status_code == 201:
            print("Registro bem-sucedido:", info.text)
            return redirect('verify_email') # alterar para pagina de verificação de email quando disponível
        else:
            print("Erro no registro. Status:", info.status_code, "Resposta:", info.text)
            return render(request, 'authentication/register.html', {'error': 'Falha no registro: ' + info.text})

    else:
        return render(request, 'authentication/register.html', {"page":"auth"})


def login_view(request):
    if request.method == 'POST':
        data = {
            "email": request.POST.get('email'),
            "password": request.POST.get('password')
        }

        info = requests.post('http://localhost:8080/auth/login', json=data)

        if info.status_code == 200 or info.status_code == 201:
            print("Login bem-sucedido:", info.text)

            name = info.json().get("name")
            token = info.json().get("token")

            request.session['name'] = name
            request.session['auth_token'] = token

            return redirect('home') # alterar para pagina de verificação de email quando disponível
        else:
            print("Erro no login. Status:", info.status_code, "Resposta:", info.text)
            return render(request, 'authentication/login.html', {'error': 'Falha no Login: ' + info.text})

    else:
        return render(request, 'authentication/login.html', {"page":"auth"})

def logout(request):
    request.session.clear()
    return redirect('login')


def verify_email_view(request):
    """Handle email verification codes submitted from `verificar_email.html`.

    POST: sends JSON {"code": <code>} to the external `/auth/verify` endpoint.
    On success redirects to `login`. On failure re-renders the verification page
    with an error message.
    """
    if request.method == 'POST':
        code = request.POST.get('code')
        if not code:
            return render(request, 'authentication/verificar_email.html', {
                'error': 'Por favor forneça o código de verificação.',
                'page': 'auth'
            })

        payload = { 'code': code }
        try:
            resp = requests.post('http://localhost:8080/auth/verify', json=payload, timeout=10)
            if resp.status_code in (200, 201):
                # verification successful
                name = resp.json().get("name")
                token = resp.json().get("token")

                request.session['name'] = name
                request.session['auth_token'] = token
                return redirect('home')
            else:
                # show API error message
                msg = resp.text or f'Status {resp.status_code}'
                return render(request, 'authentication/verificar_email.html', {
                    'error': 'Falha na verificação: ' + msg,
                    'page': 'auth'
                })
        except requests.exceptions.RequestException as e:
            return render(request, 'authentication/verificar_email.html', {
                'error': 'Erro ao conectar com o serviço de autenticação.',
                'page': 'auth'
            })

    # GET
    return render(request, 'authentication/verificar_email.html', { 'page': 'auth' })
