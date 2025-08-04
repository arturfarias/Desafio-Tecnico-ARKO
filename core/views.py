from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('states')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login/index.html')

def about(request):
    return render(request, 'about/index.html')

