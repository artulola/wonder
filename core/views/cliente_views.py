from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from accounts.decorators import cliente_required
from core.forms import UserUpdateForm, ClienteEnderecoUpdateForm
from django.db.models import Q, Count
from accounts.models import Prestador, Categoria, Servico, Agendamento, HorarioFuncionamento
from datetime import datetime, timedelta
from django.utils import timezone
from urllib.parse import unquote

@cliente_required
def cliente_home_view(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.annotate(
        num_prestadores=Count(
            'prestadores', 
            filter=Q(prestadores__status=Prestador.StatusPrestador.APROVADO)
        )
    ).order_by('-num_prestadores', 'nome')
    
    todos_aprovados = Prestador.objects.filter(status=Prestador.StatusPrestador.APROVADO)

    cidade_selecionada = request.session.get('cidade_atual')
    if cidade_selecionada:
        todos_aprovados = todos_aprovados.filter(cidade_atendimento=cidade_selecionada)
    
    prestadores_processados = []
    
    agora = timezone.localtime()
    dia_semana_hoje = (agora.weekday() + 1) % 7 
    hora_atual = agora.time()

    for p in todos_aprovados:
        if not p.tem_perfil_completo():
            continue
            
        horario_hoje = p.horarios.filter(dia_semana=dia_semana_hoje).first()
        
        is_open = False
        texto_horario = "Fechado"
        status_text = "Fechado"
        
        if horario_hoje:
            if horario_hoje.fechado:
                is_open = False
                texto_horario = "Fechado hoje"
                status_text = "Fechado hoje"
            elif horario_hoje.aberto_24h:
                is_open = True
                texto_horario = "24 horas"
                status_text = "Aberto agora"
            elif horario_hoje.hora_inicio and horario_hoje.hora_fim:
                inicio = horario_hoje.hora_inicio.strftime('%H:%M')
                fim = horario_hoje.hora_fim.strftime('%H:%M')
                texto_horario = f"{inicio} - {fim}"
                
                if horario_hoje.hora_inicio <= hora_atual <= horario_hoje.hora_fim:
                    is_open = True
                    status_text = "Aberto agora"
                else:
                    is_open = False
                    if hora_atual < horario_hoje.hora_inicio:
                        status_text = f"Abre às {inicio}"
                    else:
                        status_text = "Fechado agora"
            else:
                is_open = False
                texto_horario = "Indisponível"
        
        p.is_open_today = is_open
        p.status_text = status_text
        p.status_color = "green" if is_open else "red"
        p.horario_display = texto_horario
        
        prestadores_processados.append(p)
    
    prestadores_processados.sort(key=lambda x: x.is_open_today, reverse=True)

    context = {
        'categorias': categorias,
        'prestadores': prestadores_processados
    }
    return render(request, 'core/cliente/home.html', context)

@cliente_required
def cliente_busca_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q')
    categorias = Categoria.objects.all()
    prestadores_filtrados = []

    if query:
        resultados_banco = Prestador.objects.filter(
            Q(nome_estabelecimento__icontains=query) | 
            Q(categorias__nome__icontains=query),
            status=Prestador.StatusPrestador.APROVADO
        ).distinct()
        
        prestadores_filtrados = [p for p in resultados_banco if p.tem_perfil_completo()]
    
    context = {
        'categorias': categorias,
        'prestadores': prestadores_filtrados,
        'query': query
    }
    return render(request, 'core/cliente/busca.html', context)

@cliente_required
def cliente_cidade_view(request: HttpRequest) -> HttpResponse:
    
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
    request.session['cidade_atual'] = unquote(cidade)
    request.session.modified = True 
    
    return redirect('cliente-home')

@cliente_required
def cliente_perfil_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    
    if not hasattr(user, 'perfil_cliente'):
        messages.error(request, 'Perfil não encontrado.')
        return redirect('cliente-home')

    perfil_cliente = user.perfil_cliente

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        c_form = ClienteEnderecoUpdateForm(request.POST, instance=perfil_cliente)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, 'Perfil atualizado!')
            return redirect('cliente-perfil')
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
    prestador = get_object_or_404(Prestador, id=prestador_id)
    
    agora = timezone.localtime()
    dia_semana_hoje = (agora.weekday() + 1) % 7
    hora_atual = agora.time()
    
    horario_hoje = prestador.horarios.filter(dia_semana=dia_semana_hoje).first()
    
    is_open = False
    status_text = "Fechado"
    horario_display = "Consulte agenda"
    
    if horario_hoje:
        if horario_hoje.fechado:
            is_open = False
            status_text = "Fechado hoje"
            horario_display = "Não abre hoje"
        elif horario_hoje.aberto_24h:
            is_open = True
            status_text = "Aberto agora"
            horario_display = "24 horas"
        elif horario_hoje.hora_inicio and horario_hoje.hora_fim:
            inicio_str = horario_hoje.hora_inicio.strftime('%H:%M')
            fim_str = horario_hoje.hora_fim.strftime('%H:%M')
            horario_display = f"{inicio_str} - {fim_str}"
            
            if horario_hoje.hora_inicio <= hora_atual <= horario_hoje.hora_fim:
                is_open = True
                status_text = "Aberto agora"
            else:
                is_open = False
                if hora_atual < horario_hoje.hora_inicio:
                    status_text = f"Abre às {inicio_str}"
                else:
                    status_text = "Fechado agora"

    context = {

        'prestador': prestador,
        'horario_display': horario_display,
        'status_text': status_text,
        'status_color': "green" if is_open else "red"
    }

    return render(request, 'core/cliente/detalhe_estabelecimento.html', context)

@cliente_required
def cliente_agendamentos_view(request: HttpRequest) -> HttpResponse:
    cliente = request.user.perfil_cliente
    agendamentos = Agendamento.objects.filter(
        cliente=cliente,
        status__in=[Agendamento.StatusAgendamento.AGENDADO, Agendamento.StatusAgendamento.CONFIRMADO]
    ).order_by('data_hora_inicio')
    
    return render(request, 'core/cliente/agendados.html', {'agendamentos': agendamentos})

@cliente_required
def cliente_agendamentos_finalizados_view(request: HttpRequest) -> HttpResponse:
    cliente = request.user.perfil_cliente
    
    agendamentos = Agendamento.objects.filter(
        cliente=cliente,
        status__in=[Agendamento.StatusAgendamento.CONCLUIDO, Agendamento.StatusAgendamento.CANCELADO]
    ).order_by('-data_hora_inicio')
    
    return render(request, 'core/cliente/finalizados.html', {'agendamentos': agendamentos})

@cliente_required
def cliente_estabelecimento_oferece_view(request: HttpRequest, prestador_id: int) -> HttpResponse:

    prestador = get_object_or_404(Prestador, id=prestador_id)

    if request.method == 'POST':
        servicos_ids = request.POST.getlist('services')
        if not servicos_ids:
            messages.error(request, 'Selecione pelo menos um serviço.')
        else:
            request.session['agendamento_servicos_ids'] = servicos_ids
            request.session['agendamento_prestador_id'] = prestador_id

            return redirect('cliente-estabelecimento-horarios')
    
    servicos = Servico.objects.filter(prestador=prestador)

    context = {

        'prestador': prestador,
        'servicos': servicos

    }

    return render(request, 'core/cliente/estabelecimento_oferece.html', context)

def gerar_horarios_disponiveis(prestador, data_selecionada, duracao_total_minutos): 
    dia_semana_model = (data_selecionada.weekday() + 1) % 7
    regras = HorarioFuncionamento.objects.filter(prestador=prestador, dia_semana=dia_semana_model, fechado=False)
    if not regras.exists(): return []
    
    agendamentos = Agendamento.objects.filter(
        prestador=prestador,
        data_hora_inicio__date=data_selecionada,
        status__in=['AGENDADO', 'CONFIRMADO']
    ).order_by('data_hora_inicio')

    horarios_livres = []
    passo = timedelta(minutes=30)
    duracao_total = timedelta(minutes=duracao_total_minutos)
    agora = timezone.localtime()

    for regra in regras:
        if regra.aberto_24h:
            inicio = timezone.make_aware(datetime.combine(data_selecionada, datetime.min.time()))
            fim = timezone.make_aware(datetime.combine(data_selecionada, datetime.max.time()))
        else:
            if not regra.hora_inicio or not regra.hora_fim: continue
            inicio = timezone.make_aware(datetime.combine(data_selecionada, regra.hora_inicio))
            fim = timezone.make_aware(datetime.combine(data_selecionada, regra.hora_fim))

        if data_selecionada == agora.date():
            if inicio < agora:
                minutos_extra = 30 - (agora.minute % 30)
                inicio = agora + timedelta(minutes=minutos_extra)
                inicio = inicio.replace(second=0, microsecond=0)

        cursor = inicio
        while cursor + duracao_total <= fim:
            fim_do_slot = cursor + duracao_total
            colisao = False
            
            for ag in agendamentos:
                if (cursor < ag.data_hora_fim) and (fim_do_slot > ag.data_hora_inicio):
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
        messages.warning(request, 'Sessão expirou. Inicie o agendamento novamente.')
        return redirect('cliente-home')

    prestador = get_object_or_404(Prestador, id=prestador_id)
    servicos_objetos = Servico.objects.filter(id__in=servicos_ids)
    duracao_total = sum([s.duracao_minutos for s in servicos_objetos])

    data_get = request.GET.get('data')
    hoje = timezone.now().date()
    
    try:
        data_selecionada = datetime.strptime(data_get, '%Y-%m-%d').date() if data_get else hoje
    except ValueError:
        data_selecionada = hoje

    horarios = gerar_horarios_disponiveis(prestador, data_selecionada, duracao_total)

    if request.method == 'POST':
        hora_str = request.POST.get('selected_time')
        if not hora_str:
            messages.error(request, 'Selecione um horário.')
        else:
            try:
                data_hora_str = f"{data_selecionada.strftime('%Y-%m-%d')} {hora_str}"
                dt_inicial = timezone.make_aware(datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M"))
                
                cursor = dt_inicial
                for servico in servicos_objetos:
                    Agendamento.objects.create(
                        cliente=request.user.perfil_cliente,
                        prestador=prestador,
                        servico=servico,
                        data_hora_inicio=cursor,
                        status=Agendamento.StatusAgendamento.AGENDADO
                    )
                    cursor += timedelta(minutes=servico.duracao_minutos)
                
                del request.session['agendamento_prestador_id']
                del request.session['agendamento_servicos_ids']
                
                messages.success(request, 'Solicitação enviada com sucesso!')
                return redirect('cliente-agendamentos')

            except Exception as e:
                messages.error(request, f'Erro ao agendar: {e}')

    return render(request, 'core/cliente/estabelecimento_horarios.html', {
        'prestador': prestador,
        'horarios': horarios,
        'data_selecionada': data_selecionada,
        'hoje': hoje,
        'duracao_total': duracao_total
    })

@cliente_required
def cliente_estabelecimento_horarios_calendario_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_calendario.html')