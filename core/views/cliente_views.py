from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import cliente_required
from core.forms import UserUpdateForm, ClienteEnderecoUpdateForm
from django.db.models import Q
from accounts.models import Prestador, Categoria, Servico, Agendamento, HorarioFuncionamento
from datetime import datetime, timedelta, date
from django.utils import timezone

@cliente_required
def cliente_home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/home.html')

@cliente_required
def cliente_busca_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/busca.html')


@cliente_required
def cliente_cidade_view(request: HttpRequest) -> HttpResponse:
    """Exibe lista de cidades onde há prestadores cadastrados."""
    
    cidades_query = Prestador.objects.values_list('cidade_atendimento', flat=True).distinct().order_by('cidade_atendimento')
    
    termo = request.GET.get('q')
    if termo:
        cidades_query = cidades_query.filter(cidade_atendimento__icontains=termo)

    context = {
        'cidades': cidades_query,
        'termo_busca': termo
    }
    return render(request, 'core/cliente/cidade.html', context)

def definir_cidade_view(request: HttpRequest, cidade: str) -> HttpResponse:
    """
    Salva a cidade escolhida na sessão e redireciona para a home.
    """
    cidade_limpa = unquote(cidade)
    
    request.session['cidade_atual'] = cidade_limpa
    request.session.modified = True 
    
    return redirect('cliente-home')

@cliente_required
def cliente_perfil_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    
    if not hasattr(user, 'perfil_cliente'):
        messages.error(request, 'Perfil de cliente não encontrado.')
        return redirect('cliente-home')

    perfil_cliente = user.perfil_cliente

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        c_form = ClienteEnderecoUpdateForm(request.POST, instance=perfil_cliente)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('cliente-perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        u_form = UserUpdateForm(instance=user)
        c_form = ClienteEnderecoUpdateForm(instance=perfil_cliente)

    context = {
        'u_form': u_form,
        'c_form': c_form
    }
    return render(request, 'core/cliente/perfil.html', context)

@cliente_required
def cliente_detalhe_estabelecimento_view(request: HttpRequest, prestador_id: int) -> HttpResponse:
    """Exibe os detalhes do estabelecimento, incluindo fotos e informações de contato."""

    prestador = get_object_or_404(Prestador, id = prestador_id)

    context = {

        'prestador': prestador,
    }

    return render(request, 'core/cliente/detalhe_estabelecimento.html', context)

@cliente_required
def cliente_agendamentos_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/agendados.html')

@cliente_required
def cliente_agendamentos_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/finalizados.html')

@cliente_required
def cliente_estabelecimento_oferece_view(request: HttpRequest, prestador_id: int) -> HttpResponse:

    prestador = get_object_or_404(Prestador, id=prestador_id)

    if request.method == 'POST':
        servicos_selecionados_ids = request.POST.getlist('services')

        if not servicos_selecionados_ids:
            messages.error(request, 'Selecione pelo menos um serviço.')
        else:
            request.session['agendamento_servicos_ids'] = servicos_selecionados_ids
            request.session['agendamento_prestador_id'] = prestador_id

            return redirect('cliente-estabelecimento-horarios')
    
    servicos = Servico.objects.filter(prestador=prestador)

    context = {

        'prestador': prestador,
        'servicos': servicos

    }

    return render(request, 'core/cliente/estabelecimento_oferece.html', context)

def gerar_horarios_disponiveis(prestador, data_selecionada, duracao_total_minutos): 

    """Retorna lista de horarios disponiveis"""

    dia_semana_python = data_selecionada.weekday()
    dia_semana_model = (dia_semana_python + 1) % 7

    regras = HorarioFuncionamento.objects.filter(
        prestador=prestador,
        dia_semana=dia_semana_model,
        fechado=False
    )

    if not regras.exists():
        return []
    
    agendamentos_ocupados = Agendamento.objects.filter(
        prestador = prestador,
        data_hora_inicio__date=data_selecionada,
        status__in=[Agendamento.StatusAgendamento.AGENDADO, Agendamento.StatusAgendamento.CONFIRMADO]
    ).order_by('data_hora_inicio')

    horarios_livres = []
    passo = timedelta(minutes=30)
    duracao_total = timedelta(minutes=duracao_total_minutos)
    agora = timezone.localtime().replace(tzinfo=None)

    for regra in regras:
        # Define inicio e fim do expediente
        if regra.aberto_24h:
            inicio_expediente = datetime.combine(data_selecionada, datetime.min.time())
            fim_expediente = datetime.combine(data_selecionada, datetime.max.time())
        else:
            if not regra.hora_inicio or not regra.hora_fim:
                continue
            inicio_expediente = datetime.combine(data_selecionada, regra.hora_inicio)
            fim_expediente = datetime.combine(data_selecionada, regra.hora_fim)

        if data_selecionada == agora.date():
            if inicio_expediente < agora:
                minutos = agora.minute
                delta = 30 - (minutos % 30) if (minutos % 30) != 0 else 0
                inicio_expediente = (agora + timedelta(minutes=delta)).replace(second=0, microsecond=0)

        cursor = inicio_expediente
        while cursor + duracao_total <= fim_expediente:
            fim_do_slot = cursor + duracao_total
            colisao = False
            
            for agendamento in agendamentos_ocupados:
             
                ag_inicio = timezone.make_naive(agendamento.data_hora_inicio)
                ag_fim = timezone.make_naive(agendamento.data_hora_fim)
                
                if (cursor < ag_fim) and (fim_do_slot > ag_inicio):
                    colisao = True
                    break
            
            if not colisao:
                horarios_livres.append({
                    'inicio': cursor.strftime('%H:%M'),
                    'fim': fim_do_slot.strftime('%H:%M'),
                    'value': cursor.strftime('%H:%M') 
                })

            cursor += passo

    return horarios_livres


@cliente_required
def cliente_estabelecimento_horarios_view(request: HttpRequest) -> HttpResponse:
    
    prestador_id = request.session.get('agendamento_prestador_id')
    servicos_ids = request.session.get('agendamento_servicos_ids')

    if not prestador_id or not servicos_ids:
        messages.warning(request, 'Por favor, inicie o agendamento novamente.')
        return redirect('cliente-home')

    prestador = get_object_or_404(Prestador, id=prestador_id)
    servicos_objetos = Servico.objects.filter(id__in=servicos_ids)
    
    duracao_total_minutos = sum([s.duracao_minutos for s in servicos_objetos])

    data_get = request.GET.get('data')
    try:
        if data_get:
            data_selecionada = datetime.strptime(data_get, '%Y-%m-%d').date()
        else:
            data_selecionada = timezone.now().date()
    except ValueError:
        data_selecionada = timezone.now().date()

    horarios = gerar_horarios_disponiveis(prestador, data_selecionada, duracao_total_minutos)

    if request.method == 'POST':
        hora_inicio_str = request.POST.get('selected_time')

        if not hora_inicio_str:
            messages.error(request, 'Selecione um horário para continuar.')
        else:
            try:
                data_hora_inicial = datetime.strptime(f"{data_selecionada} {hora_inicio_str}", "%Y-%m-%d %H:%M")
                
                cursor_tempo = data_hora_inicial

                for servico in servicos_objetos:
                    Agendamento.objects.create(
                        cliente=request.user.perfil_cliente,
                        prestador=prestador,
                        servico=servico,
                        data_hora_inicio=cursor_tempo,
                        status=Agendamento.StatusAgendamento.AGENDADO
                    )
                    cursor_tempo += timedelta(minutes=servico.duracao_minutos)
                
                del request.session['agendamento_prestador_id']
                del request.session['agendamento_servicos_ids']
                
                messages.success(request, 'Agendamento realizado com sucesso!')
                return redirect('cliente-agendamentos') 

            except Exception as e:
                messages.error(request, f'Erro ao processar agendamento: {str(e)}')

    context = {
        'prestador': prestador,
        'horarios': horarios,
        'data_selecionada': data_selecionada,
        'hoje': timezone.now().date(),
        'duracao_total': duracao_total_minutos
    }

    return render(request, 'core/cliente/estabelecimento_horarios.html', context)

@cliente_required
def cliente_estabelecimento_horarios_calendario_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_calendario.html')

@cliente_required
def cliente_busca_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q')
    categorias = Categoria.objects.all()
    prestadores_filtrados = []

    if query:
        # Busca inicial no banco (filtra por nome, categoria E status APROVADO)
        resultados_banco = Prestador.objects.filter(
            Q(nome_estabelecimento__icontains=query) | 
            Q(categorias__nome__icontains=query),
            status=Prestador.StatusPrestador.APROVADO
        ).distinct()
        
        # Filtra na memória para exibir APENAS os que têm perfil completo
        prestadores_filtrados = [
            p for p in resultados_banco 
            if p.tem_perfil_completo()
        ]
    
    context = {
        'categorias': categorias,
        'prestadores': prestadores_filtrados,
        'query': query
    }

    return render(request, 'core/cliente/busca.html', context)

    