from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_cliente_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home.html')

def search(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/busca.html')

def search_results_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/resultado-busca.html')

def login_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/login.html')

def cadastro_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cadastro.html')

def register_options_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/opcao-cadastro.html')

def cidade_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cidade.html')

def perfil_usuario_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/perfil-usuario.html')

def detalhe_estabelecimento_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/detalhe_estabelecimento.html')

def agendamento_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/agendamento/agendados.html')

def agendamentos_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/agendamento/finalizados.html')

def cadastro_prestador_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cadastro_prestador.html')

def solicitacoes_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/solicitacoes.html')



def home_prestador_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home_prestador.html')
  
def solicitacoes_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/solicitacoes.html')

def detalhes_solicitacoes_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/detalhes-solicitacoes.html')

def categorias_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/categorias.html')


def home_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home_finalizados.html')

def home_cancelados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home_cancelados.html')

def perfil_prestador_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/perfil_prestador.html')