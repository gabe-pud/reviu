from django.shortcuts import render, redirect
import requests

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        print(request.POST.get('password'))
        data = {
            "email": request.POST.get('email'),
            "password": request.POST.get('password')
        }

        info = requests.post('http://localhost:8080/auth/login', json=data)
        print(info)

        if info.status_code == 200 or info.status_code == 201:
            print("Login bem-sucedido:", info.text)
            return redirect('login') # alterar para pagina de verificação de email quando disponível
        else:
            print("Erro no login. Status:", info.status_code, "Resposta:", info.text)
            return render(request, 'authentication/login.html', {'error': 'Falha no Login: ' + info.text})

    else:
        return render(request, 'authentication/login.html')
