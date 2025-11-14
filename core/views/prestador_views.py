from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def prestador_home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/home.html')

def prestador_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/finalizados.html')

def prestador_cancelados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/cancelados.html')

def prestador_perfil_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/perfil.html')