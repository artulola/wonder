"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_cliente_view, name='home-cliente'),
    path('busca/', views.search, name= 'search'),
    path('busca/resultado-busca/', views.search_results_view, name='resultado-busca'),
    path('login/', views.login_view, name='login' ),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('opcoes-cadastro/', views.register_options_view, name='opcoes-cadastro'),
    path('cidade/', views.cidade_view, name='cidade'),
    path('perfil-usuario/', views.perfil_usuario_view, name='perfil-usuario'),
    path('detalhe-estabelecimento/', views.detalhe_estabelecimento_view, name='detalhe-estabelecimento'),
    path('agendamentos/', views.agendamento_view, name='agendamento'),
    path('agendamentos/finalizados/', views.agendamentos_finalizados_view, name='agendamentos-finalizados'),
    path('cadastro-prestador/', views.cadastro_prestador_view, name='cadastro-prestador'),
    path('solicitacoes/', views.solicitacoes_view, name='solicitacoes'),
    path('home_prestador/', views.home_prestador_view, name='home_prestador'),
    path('solicitacoes/detalhes-solicitacoes/', views.detalhes_solicitacoes_view, name='detalhes-solicitacoes'),
    
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
