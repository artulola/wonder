import json
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import prestador_required
from core.forms import UserUpdateForm, PrestadorEstabelecimentoUpdateForm
from accounts.models import Servico, Categoria, Agendamento, HorarioFuncionamento, FotoEstabelecimento


@prestador_required
def prestador_home_view(request: HttpRequest) -> HttpResponse:
    prestador = request.user.perfil_prestador

    agora = timezone.now()
    Agendamento.objects.filter(
        prestador=prestador,
        status=Agendamento.StatusAgendamento.AGENDADO,
        data_hora_inicio__lt=agora
    ).update(
        status=Agendamento.StatusAgendamento.CANCELADO,
        motivo_cancelamento="Sistema: Solicitação expirada."
    )

    data_str = request.GET.get('data')
    if data_str:
        try:
            data_escolhida = timezone.datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            data_escolhida = timezone.localtime(timezone.now()).date()
    else:
        data_escolhida = timezone.localtime(timezone.now()).date()

    agendamentos = Agendamento.objects.filter(
        prestador=prestador,
        data_hora_inicio__date=data_escolhida,
        status__in=[Agendamento.StatusAgendamento.AGENDADO, Agendamento.StatusAgendamento.CONFIRMADO]
    ).order_by('data_hora_inicio')

    media = prestador.avaliacoes.aggregate(Avg('nota'))['nota__avg']
    media_avaliacao = round(media, 1) if media else None
    total_avaliacoes = prestador.avaliacoes.count()

    return render(request, 'core/prestador/home.html', {
        'agendamentos': agendamentos,
        'data_escolhida': data_escolhida,
        'media_avaliacao': media_avaliacao,
        'total_avaliacoes': total_avaliacoes
    })


@prestador_required
def finalizar_agendamento_view(request: HttpRequest, agendamento_id: int) -> HttpResponse:
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, prestador=request.user.perfil_prestador)
    agendamento.status = Agendamento.StatusAgendamento.CONCLUIDO
    agendamento.save()
    messages.success(request, 'Agendamento finalizado com sucesso!')
    return redirect('prestador-home')


@prestador_required
def confirmar_agendamento_view(request: HttpRequest, agendamento_id: int) -> HttpResponse:
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, prestador=request.user.perfil_prestador)
    
    if agendamento.status == Agendamento.StatusAgendamento.AGENDADO:
        agendamento.status = Agendamento.StatusAgendamento.CONFIRMADO
        agendamento.save()
        messages.success(request, 'Agendamento confirmado com sucesso!')
    else:
        messages.warning(request, 'Este agendamento não está pendente.')
        
    return redirect('prestador-home')


@prestador_required
def cancelar_agendamento_view(request: HttpRequest, agendamento_id: int) -> HttpResponse:
    
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, prestador=request.user.perfil_prestador)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', 'Cancelado pelo prestador.')
        agendamento.status = Agendamento.StatusAgendamento.CANCELADO
        agendamento.motivo_cancelamento = motivo
        agendamento.save()
        messages.warning(request, 'Agendamento cancelado.')
        return redirect('prestador-home')
    
    return render(request, 'core/prestador/cancelar_agendamento.html', {'agendamento': agendamento})


@prestador_required
def prestador_finalizados_view(request: HttpRequest) -> HttpResponse:
    prestador = request.user.perfil_prestador
    
    finalizados = Agendamento.objects.filter(
        prestador=prestador, 
        status=Agendamento.StatusAgendamento.CONCLUIDO
    ).order_by('-data_hora_inicio')
    
    return render(request, 'core/prestador/finalizados.html', {'agendamentos': finalizados})


@prestador_required
def prestador_cancelados_view(request: HttpRequest) -> HttpResponse:
    
    prestador = request.user.perfil_prestador
    
    cancelados = Agendamento.objects.filter(
        prestador=prestador, 
        status=Agendamento.StatusAgendamento.CANCELADO
    ).order_by('-data_hora_inicio')
    
    return render(request, 'core/prestador/cancelados.html', {'agendamentos': cancelados})


@prestador_required
def prestador_perfil_view(request: HttpRequest) -> HttpResponse:
    user = request.user

    if not hasattr(user, 'perfil_prestador'):
        messages.error(request, 'Perfil de prestador não encontrado.')
        return redirect('cliente-home')

    perfil_prestador = user.perfil_prestador
    servicos = Servico.objects.filter(prestador=perfil_prestador)
    fotos_estabelecimento = FotoEstabelecimento.objects.filter(prestador=perfil_prestador)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'atualizar_perfil':
            u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            p_form = PrestadorEstabelecimentoUpdateForm(request.POST, instance=perfil_prestador)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('prestador-perfil')
            else:
                messages.error(request, 'Erro ao atualizar. Verifique os dados.')

        elif acao == 'criar_servico':
            try:
                nome = request.POST.get('nome')
                descricao = request.POST.get('descricao')
                preco = request.POST.get('preco')
                duracao = request.POST.get('duracao')
                foto = request.FILES.get('foto')
                servico = Servico.objects.create(
                    prestador=perfil_prestador,
                    nome=nome,
                    descricao=descricao,
                    preco=preco,
                    duracao_minutos=duracao,
                    foto=foto
                )
                servico.categorias.set(request.POST.getlist('categorias'))
                messages.success(request, 'Serviço criado com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao criar serviço: {e}')
            return redirect('prestador-perfil')

        elif acao == 'editar_servico':
            servico_id = request.POST.get('servico_id')
            servico = get_object_or_404(Servico, id=servico_id, prestador=perfil_prestador)
            servico.nome = request.POST.get('nome')
            servico.descricao = request.POST.get('descricao')
            servico.preco = request.POST.get('preco')
            servico.duracao_minutos = request.POST.get('duracao')
            if 'foto' in request.FILES:
                servico.foto = request.FILES['foto']
            servico.save()
            servico.categorias.set(request.POST.getlist('categorias'))
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('prestador-perfil')

        elif acao == 'excluir_servico':
            servico_id = request.POST.get('servico_id')
            servico = get_object_or_404(Servico, id=servico_id, prestador=perfil_prestador)
            servico.delete()
            messages.success(request, 'Serviço excluído com sucesso!')
            return redirect('prestador-perfil')
        
        elif acao == 'adicionar_foto_local':
            if 'foto_local' in request.FILES:
                imagem = request.FILES['foto_local']
                try:
                    FotoEstabelecimento.objects.create(prestador=perfil_prestador, imagem=imagem)
                    messages.success(request, 'Foto adicionada com sucesso!')
                except Exception as e:
                    messages.error(request, f'Erro ao salvar foto: {e}')
            else:
                messages.error(request, 'Nenhuma imagem selecionada.')
            return redirect('prestador-perfil')   

        elif acao == 'excluir_foto_local':
            foto_id = request.POST.get('foto_id')
            foto = get_object_or_404(FotoEstabelecimento, id=foto_id, prestador=perfil_prestador)
            foto.delete()
            messages.success(request, 'Foto removida com sucesso!')
            return redirect('prestador-perfil')

        elif acao == 'atualizar_horarios':
            json_data = request.POST.get('horarios_json_completo')
            
            if json_data:
                try:
                    dados_horarios = json.loads(json_data)
                    
                    HorarioFuncionamento.objects.filter(prestador=perfil_prestador).delete()
                  
                    for dia_index, info in dados_horarios.items():
                        dia_int = int(dia_index)
                        eh_24h = info.get('aberto_24h', False)
                        eh_fechado = info.get('fechado', False)

                        if eh_24h or eh_fechado:
                            HorarioFuncionamento.objects.create(
                                prestador=perfil_prestador,
                                dia_semana=dia_int,
                                aberto_24h=eh_24h,
                                fechado=eh_fechado
                            )
                        else:
                            intervalos = info.get('intervalos', [])
                            for intervalo in intervalos:
                                inicio = intervalo.get('inicio')
                                fim = intervalo.get('fim')
                                if inicio and fim:
                                    HorarioFuncionamento.objects.create(
                                        prestador=perfil_prestador,
                                        dia_semana=dia_int,
                                        hora_inicio=inicio,
                                        hora_fim=fim,
                                        aberto_24h=False,
                                        fechado=False
                                    )
                    messages.success(request, 'Horários atualizados com sucesso!')
                except Exception as e:
                    messages.error(request, 'Erro ao salvar horários.')
            
            return redirect('prestador-perfil')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = PrestadorEstabelecimentoUpdateForm(instance=perfil_prestador)

    horarios_banco = HorarioFuncionamento.objects.filter(prestador=perfil_prestador)
    horarios_dict = {}

    for h in horarios_banco:
        d = str(h.dia_semana)
        if d not in horarios_dict:
            horarios_dict[d] = {
                'aberto_24h': h.aberto_24h,
                'fechado': h.fechado,
                'intervalos': []
            }
        
        if not h.aberto_24h and not h.fechado and h.hora_inicio and h.hora_fim:
            horarios_dict[d]['intervalos'].append({
                'inicio': h.hora_inicio.strftime('%H:%M'),
                'fim': h.hora_fim.strftime('%H:%M')
            })
            horarios_dict[d]['aberto_24h'] = False
            horarios_dict[d]['fechado'] = False

    horarios_json = json.dumps(horarios_dict)

    dias_semana = [
        (0, 'Domingo'), (1, 'Segunda-feira'), (2, 'Terça-feira'), 
        (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado')
    ]

    pendencias = []
    if not user.foto_perfil:
        pendencias.append("Adicionar uma foto de perfil")
    
    if not FotoEstabelecimento.objects.filter(prestador=perfil_prestador).exists():
        pendencias.append("Adicionar pelo menos uma foto do estabelecimento")
    
    if not HorarioFuncionamento.objects.filter(prestador=perfil_prestador).exists():
        pendencias.append("Configurar os horários de funcionamento")

    if not Servico.objects.filter(prestador=perfil_prestador).exists():
        pendencias.append("Cadastrar pelo menos um serviço")

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'prestador': perfil_prestador,
        'servicos': servicos,
        'categorias': categorias,
        'fotos_estabelecimento': fotos_estabelecimento,
        'dias_semana': dias_semana,
        'horarios_json': horarios_json,
        'pendencias': pendencias
    }
    return render(request, 'core/prestador/perfil.html', context)