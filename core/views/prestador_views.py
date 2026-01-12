from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from accounts.decorators import prestador_required
from core.forms import UserUpdateForm, PrestadorEstabelecimentoUpdateForm

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

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        p_form = PrestadorEstabelecimentoUpdateForm(request.POST, instance=perfil_prestador)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('prestador-perfil')
        else:
            messages.error(request, 'Erro ao atualizar. Verifique os dados.')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = PrestadorEstabelecimentoUpdateForm(instance=perfil_prestador)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'prestador': perfil_prestador
    }
    return render(request, 'core/prestador/perfil.html', context)