from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import admin_views, auth_views, cliente_views, prestador_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', cliente_views.cliente_home_view, name='cliente-home'),
    path('cliente/busca/', cliente_views.cliente_busca_view, name= 'cliente-busca'),
    path('cliente/busca/resultado-busca/', cliente_views.cliente_resultado_busca_view, name='cliente-resultado--busca'),
    path('cliente/cidade/', cliente_views.cliente_cidade_view, name='cliente-cidade'),
    path('cliente/perfil/', cliente_views.cliente_perfil_view, name='cliente-perfil'),
    path('cliente/estabelecimento/detalhes', cliente_views.cliente_detalhe_estabelecimento_view, name='cliente-estabelecimento--detalhe'),
    path('cliente/agendamentos/agendados', cliente_views.cliente_agendamentos_view, name='cliente-agendamentos'),
    path('cliente/agendamentos/finalizados/', cliente_views.cliente_agendamentos_finalizados_view, name='cliente-agendamentos--finalizados'),
    path('cliente/estabelecimento/oferece/', cliente_views.cliente_estabelecimento_oferece_view, name='cliente-estabelecimento--oferece'),

    path('auth/login/', auth_views.auth_login_view, name='login' ),
    path('auth/cadastro/', auth_views.auth_cadastro_view, name='cadastro'),
    path('auth/opcoes-cadastro/', auth_views.auth_opcoes_cadastro_view, name='opcoes-cadastro'),
    path('auth/cadastro-prestador/', auth_views.auth_cadastro_prestador_view, name='cadastro-prestador'),
    path('auth/aguardando_aprovacao/', auth_views.auth_aguardando_aprovacao_view, name='aguardando_aprovacao'),

    path('ad/solicitacoes/', admin_views.admin_solicitacoes_view, name='admin-solicitacoes'),
    path('ad/solicitacoes/detalhes-solicitacao/', admin_views.admin_detalhes_solicitacoes_view, name='admin-detalhes--solicitacao'),
    path('ad/categorias/', admin_views.admin_categorias_view, name='admin-categorias'),

    path('prestador/finalizados/', prestador_views.prestador_finalizados_view, name='prestador-finalizados'),
    path('prestador/cancelados/', prestador_views.prestador_cancelados_view, name='prestador-cancelados'),
    path('prestador/perfil', prestador_views.prestador_perfil_view, name='prestador-perfil'),
    path('prestador/home/', prestador_views.prestador_home_view, name='prestador-home'),
 
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
