from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import cliente_required
from core.forms import UserUpdateForm, ClienteEnderecoUpdateForm

@cliente_required
def cliente_home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/home.html')

@cliente_required
def cliente_busca_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/busca.html')

@cliente_required
def cliente_resultado_busca_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/resultado_busca.html')

@cliente_required
def cliente_cidade_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/cidade.html')

@cliente_required
def cliente_perfil_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    
    if not hasattr(user, 'perfil_cliente'):
        messages.error(request, 'Perfil de cliente não encontrado.')
        return redirect('home-cliente')

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
def cliente_detalhe_estabelecimento_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/detalhe_estabelecimento.html')

@cliente_required
def cliente_agendamentos_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/agendados.html')

@cliente_required
def cliente_agendamentos_finalizados_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/finalizados.html')

@cliente_required
def cliente_estabelecimento_oferece_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_oferece.html')

@cliente_required
def cliente_estabelecimento_horarios_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_horarios.html')

@cliente_required
def cliente_estabelecimento_horarios_calendario_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/cliente/estabelecimento_calendario.html')
