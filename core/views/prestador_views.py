from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from accounts.decorators import prestador_required
from core.forms import UserUpdateForm, PrestadorEstabelecimentoUpdateForm
from accounts.models import Servico, Categoria

@prestador_required
def prestador_home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/home.html')

@prestador_required
def prestador_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/finalizados.html')

@prestador_required
def prestador_cancelados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/prestador/cancelados.html')

@prestador_required
def prestador_perfil_view(request: HttpRequest) -> HttpResponse:
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