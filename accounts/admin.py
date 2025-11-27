from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, Categoria, Cliente, Prestador, 
    Servico, Agendamento, Avaliacao
)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'tipo_usuario', 'is_active')
    list_filter = ('tipo_usuario', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone')}),
        ('Tipo de Usuário', {'fields': ('tipo_usuario',)}),
        ('Foto de Perfil', {'fields': ('foto_perfil',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas', {'fields': ('date_joined', 'last_login')}),
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'endereco')
    search_fields = ('usuario__email', 'endereco')
    readonly_fields = ('usuario',)


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ('get_nome_profissional', 'nome_estabelecimento', 'status', 'cidade_atendimento')
    list_filter = ('status', 'cidade_atendimento')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'nome_estabelecimento', 'documento')
    filter_horizontal = ('categorias',)
    readonly_fields = ('usuario',)

    def get_nome_profissional(self, obj):
        return obj.usuario.get_full_name()
    get_nome_profissional.short_description = "Profissional"


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prestador', 'preco', 'duracao_minutos')
    list_filter = ('prestador', 'categorias')
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('categorias',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('servico', 'cliente', 'prestador', 'data_hora_inicio', 'status')
    list_filter = ('status', 'data_hora_inicio')
    search_fields = ('servico__nome', 'cliente__usuario__email')
    readonly_fields = ('cliente', 'prestador', 'servico')
    

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('agendamento', 'nota')
    list_filter = ('nota',)
    search_fields = ('agendamento__servico__nome',)
    readonly_fields = ('agendamento',)