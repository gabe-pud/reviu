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
            return redirect('register') # alterar para pagina de verificação de email quando disponível
        else:
            print("Erro no registro. Status:", info.status_code, "Resposta:", info.text)
            return render(request, 'authentication/register.html', {'error': 'Falha no registro: ' + info.text})

    else:
        return render(request, 'authentication/register.html')