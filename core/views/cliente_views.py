from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def cliente_home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/home.html')

def cliente_busca_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/busca.html')

def cliente_resultado_busca_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/resultado_busca.html')

def cliente_cidade_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/cidade.html')

def cliente_perfil_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/perfil.html')

def cliente_detalhe_estabelecimento_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/detalhe_estabelecimento.html')

def cliente_agendamentos_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/agendados.html')

def cliente_agendamentos_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/finalizados.html')

def cliente_estabelecimento_oferece_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_oferece.html')