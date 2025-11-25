from django.shortcuts import render,redirect
import requests

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            senha = request.POST.get('password1')
        else:
            return render(request, 'authentication/register.html', {'error': 'As senhas não conferem.', 'page': 'auth'})

        data = {
            "name": request.POST.get('name'),
            "username": request.POST.get('name'),
            "email": request.POST.get('email'),
            "password": senha
        }

        try:
            info = requests.post('http://localhost:8080/auth/register', json=data, timeout=10)
            if info.status_code in (200, 201):
                print("Registro bem-sucedido:", info.text)
                return redirect('verify_email')
            else:
                print("Erro no registro. Status:", info.status_code, "Resposta:", info.text)
                return render(request, 'authentication/register.html', {'error': 'Falha no registro: ' + info.text, 'page': 'auth'})
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com serviço de autenticação: {e}")
            return render(request, 'authentication/register.html', {'error': 'Erro ao conectar com o serviço de autenticação.', 'page': 'auth'})

    else:
        return render(request, 'authentication/register.html', {"page":"auth"})


def login_view(request):
    if request.method == 'POST':
        data = {
            "email": request.POST.get('email'),
            "password": request.POST.get('password')
        }
        try:
            info = requests.post('http://localhost:8080/auth/login', json=data, timeout=10)
            if info.status_code in (200, 201):
                print("Login bem-sucedido:", info.text)

                name = info.json().get("name")
                token = info.json().get("token")

                request.session['name'] = name
                request.session['auth_token'] = token

                return redirect('home')
            else:
                print("Erro no login. Status:", info.status_code, "Resposta:", info.text)
                return render(request, 'authentication/login.html', {'error': 'Falha no Login: ' + str(info.status_code), 'page': 'auth'})
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com serviço de autenticação: {e}")
            return render(request, 'authentication/login.html', {'error': 'Erro ao conectar com o serviço de autenticação.', 'page': 'auth'})

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
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com serviço de autenticação: {e}")
            return render(request, 'authentication/verificar_email.html', {
                'error': 'Erro ao conectar com o serviço de autenticação.',
                'page': 'auth'
            })

        if resp.status_code in (200, 201):
            # verification successful
            try:
                name = resp.json().get("name")
                token = resp.json().get("token")
                if name:
                    request.session['name'] = name
                if token:
                    request.session['auth_token'] = token
            except Exception:
                pass
            return redirect('home')
        else:
            # show API error message
            msg = resp.text or f'Status {resp.status_code}'
            return render(request, 'authentication/verificar_email.html', {
                'error': 'Falha na verificação: ' + msg,
                'page': 'auth'
            })

    # GET
    return render(request, 'authentication/verificar_email.html', { 'page': 'auth' })
