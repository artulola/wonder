from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def auth_login_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/login.html')

def auth_cadastro_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/cadastro.html')

def auth_opcoes_cadastro_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/opcoes_cadastro.html')

def auth_cadastro_prestador_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/cadastro_prestador.html')

def auth_aguardando_aprovacao_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/aguardando_aprovacao.html')