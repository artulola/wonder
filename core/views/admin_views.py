from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def admin_solicitacoes_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/solicitacoes.html')

def admin_detalhes_solicitacoes_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/detalhes_solicitacao.html')

def admin_categorias_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/categorias.html')