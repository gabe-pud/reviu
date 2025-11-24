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
        print(info)

        if info.status_code == 200 or info.status_code == 201:
            print("Registro bem-sucedido:", info.text)
            return redirect('login') # alterar para pagina de verificação de email quando disponível
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
        print(info)

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