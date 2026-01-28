from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import admin_views, cliente_views, prestador_views
from accounts import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', cliente_views.cliente_home_view, name='cliente-home'),
    path('busca/', cliente_views.cliente_busca_view, name='cliente-busca'),
    path('cidade/', cliente_views.cliente_cidade_view, name='cliente-cidade'),
    path('perfil/', cliente_views.cliente_perfil_view, name='cliente-perfil'),
    path('estabelecimento/<int:prestador_id>/', cliente_views.cliente_detalhe_estabelecimento_view, name='cliente-estabelecimento--detalhe'),
    path('agendamentos/agendados', cliente_views.cliente_agendamentos_view, name='cliente-agendamentos'),
    path('agendamentos/finalizados/', cliente_views.cliente_agendamentos_finalizados_view, name='cliente-agendamentos--finalizados'),
    path('estabelecimento/<int:prestador_id>/servicos/', cliente_views.cliente_estabelecimento_oferece_view, name='cliente-estabelecimento--oferece'),
    path('estabelecimento_horarios/', cliente_views.cliente_estabelecimento_horarios_view, name='cliente-estabelecimento-horarios'),
    path('estabelecimento-horarios/calendario/', cliente_views.cliente_estabelecimento_horarios_calendario_view, name='cliente-estabelecimento-horarios-calendario'),
    path('estabelecimento/horarios/',cliente_views.cliente_estabelecimento_horarios_view, name='cliente-estabelecimento-horarios'),
    path('definir-cidade/<str:cidade>/', cliente_views.definir_cidade_view, name='definir-cidade'),

    path('auth/login/', auth_views.auth_login_view, name='login' ),
    path('auth/logout/', auth_views.auth_logout_view, name='logout' ),
    path('auth/cadastro/', auth_views.auth_cadastro_view, name='cadastro'),
    path('auth/opcoes-cadastro/', auth_views.auth_opcoes_cadastro_view, name='opcoes-cadastro'),
    path('auth/cadastro-prestador/', auth_views.auth_cadastro_prestador_view, name='cadastro-prestador'),
    path('auth/aguardando_aprovacao/', auth_views.auth_aguardando_aprovacao_view, name='aguardando_aprovacao'),

    path('administrador/solicitacoes/', admin_views.admin_solicitacoes_view, name='admin-solicitacoes'),
    path('administrador/solicitacoes/detalhes-solicitacao/<int:prestador_id>/', admin_views.admin_detalhes_solicitacoes_view, name='admin-detalhes--solicitacao'),
    path('administrador/categorias/', admin_views.admin_categorias_view, name='admin-categorias'),

    path('prestador/finalizados/', prestador_views.prestador_finalizados_view, name='prestador-finalizados'),
    path('prestador/cancelados/', prestador_views.prestador_cancelados_view, name='prestador-cancelados'),
    path('prestador/perfil', prestador_views.prestador_perfil_view, name='prestador-perfil'),
    path('prestador/home/', prestador_views.prestador_home_view, name='prestador-home'),
    path('prestador/agendamentos/', prestador_views.prestador_home_view, name='prestador-agendamentos'),
    path('prestador/agendamentos/confirmar/<int:agendamento_id>/', prestador_views.confirmar_agendamento_view, name='confirmar-agendamento'), # NOVA
    path('prestador/agendamentos/finalizar/<int:agendamento_id>/', prestador_views.finalizar_agendamento_view, name='finalizar-agendamento'),
    path('agendamentos/cancelar/<int:agendamento_id>/', cliente_views.cliente_cancelar_agendamento_view, name='cliente-cancelar-agendamento'),
 
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

