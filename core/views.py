from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_cliente_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home.html')

def search(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/busca.html')

def search_results_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/resultado-busca.html')

def register_options_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/opcao-cadastro.html')
