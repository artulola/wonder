from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/base.html')

def search(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/busca.html')

def search_results_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/resultado-busca.html')

def login_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/login.html')

def cadastro_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cadastro.html')