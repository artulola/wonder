from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import prestador_required
from core.forms import UserUpdateForm, PrestadorEstabelecimentoUpdateForm
from accounts.models import Servico, Categoria, Agendamento


@prestador_required
def prestador_home_view(request: HttpRequest) -> HttpResponse:
    """
    Página inicial do prestador: lista agendamentos em aberto para o dia ou para a data escolhida.
    """
    prestador = request.user.perfil_prestador

    # Se o usuário escolher uma data via GET (?data=2026-01-20)
    data_str = request.GET.get('data')
    if data_str:
        try:
            data_escolhida = timezone.datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            data_escolhida = timezone.now().date()
    else:
        data_escolhida = timezone.now().date()

    agendamentos = Agendamento.objects.filter(
        prestador=prestador,
        data_hora_inicio__date=data_escolhida,
        status__in=[Agendamento.StatusAgendamento.AGENDADO, Agendamento.StatusAgendamento.CONFIRMADO]
    )

    return render(request, 'core/prestador/home.html', {
        'agendamentos': agendamentos,
        'data_escolhida': data_escolhida
    })


@prestador_required
def finalizar_agendamento_view(request: HttpRequest, agendamento_id: int) -> HttpResponse:
    """
    Finaliza um agendamento (status -> CONCLUIDO).
    """
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, prestador=request.user.perfil_prestador)
    agendamento.status = Agendamento.StatusAgendamento.CONCLUIDO
    agendamento.save()
    messages.success(request, 'Agendamento finalizado com sucesso!')
    return redirect('prestador-home')


@prestador_required
def cancelar_agendamento_view(request: HttpRequest, agendamento_id: int) -> HttpResponse:
    """
    Cancela um agendamento (status -> CANCELADO).
    """
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, prestador=request.user.perfil_prestador)
    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '')
        agendamento.status = Agendamento.StatusAgendamento.CANCELADO
        agendamento.motivo_cancelamento = motivo
        agendamento.save()
        messages.warning(request, 'Agendamento cancelado.')
        return redirect('prestador-home')
    return render(request, 'core/prestador/cancelar_agendamento.html', {'agendamento': agendamento})


@prestador_required
def prestador_finalizados_view(request: HttpRequest) -> HttpResponse:
    """
    Lista agendamentos finalizados.
    """
    prestador = request.user.perfil_prestador
    finalizados = Agendamento.objects.filter(prestador=prestador, status=Agendamento.StatusAgendamento.CONCLUIDO)
    return render(request, 'core/prestador/finalizados.html', {'agendamentos': finalizados})


@prestador_required
def prestador_cancelados_view(request: HttpRequest) -> HttpResponse:
    """
    Lista agendamentos cancelados.
    """
    prestador = request.user.perfil_prestador
    cancelados = Agendamento.objects.filter(prestador=prestador, status=Agendamento.StatusAgendamento.CANCELADO)
    return render(request, 'core/prestador/cancelados.html', {'agendamentos': cancelados})


@prestador_required
def prestador_perfil_view(request: HttpRequest) -> HttpResponse:
    """
    Página de perfil do prestador: atualizar dados e gerenciar serviços.
    """
    user = request.user

    if not hasattr(user, 'perfil_prestador'):
        messages.error(request, 'Perfil de prestador não encontrado.')
        return redirect('cliente-home')

    perfil_prestador = user.perfil_prestador
    servicos = Servico.objects.filter(prestador=perfil_prestador)
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

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = PrestadorEstabelecimentoUpdateForm(instance=perfil_prestador)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'prestador': perfil_prestador,
        'servicos': servicos,
        'categorias': categorias
    }
    return render(request, 'core/prestador/perfil.html', context)