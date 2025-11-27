from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.forms import ClienteRegistrationForm, PrestadorRegistrationForm, PrestadorProfileForm, ClienteEnderecoForm
from accounts.models import Cliente, Prestador, Categoria


def auth_login_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/login.html')


def auth_cadastro_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        endereco_form = ClienteEnderecoForm(request.POST)
        
        if form.is_valid() and endereco_form.is_valid():
            try:
                user = form.save()
                
                cliente = Cliente.objects.create(
                    usuario=user,
                    endereco=endereco_form.cleaned_data['endereco']
                )
                
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('cliente-home')
            
            except Exception as e:
                messages.error(request, f'Erro ao criar cadastro: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            for field, errors in endereco_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ClienteRegistrationForm()
        endereco_form = ClienteEnderecoForm()
    
    context = {
        'form': form,
        'endereco_form': endereco_form
    }
    return render(request, 'core/auth/cadastro.html', context)


def auth_opcoes_cadastro_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/opcoes_cadastro.html')


def auth_cadastro_prestador_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = PrestadorRegistrationForm(request.POST)
        prestador_form = PrestadorProfileForm(request.POST)
        
        if user_form.is_valid() and prestador_form.is_valid():
            try:
                user = user_form.save()
                
                prestador = Prestador.objects.create(
                    usuario=user,
                    nome_estabelecimento=prestador_form.cleaned_data['nome_estabelecimento'],
                    tipo_documento=prestador_form.cleaned_data['tipo_documento'],
                    documento=prestador_form.cleaned_data['documento'],
                    endereco=prestador_form.cleaned_data['endereco'],
                    cidade_atendimento=prestador_form.cleaned_data['cidade_atendimento'],
                    status=Prestador.StatusPrestador.PENDENTE
                )
                
                prestador.categorias.set(prestador_form.cleaned_data['categorias'])
                
                messages.success(request, 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.')
                return redirect('aguardando_aprovacao')
            
            except Exception as e:
                messages.error(request, f'Erro ao criar cadastro: {str(e)}')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            for field, errors in prestador_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        user_form = PrestadorRegistrationForm()
        prestador_form = PrestadorProfileForm()
    
    context = {
        'user_form': user_form,
        'prestador_form': prestador_form,
        'categorias': Categoria.objects.all()
    }
    return render(request, 'core/auth/cadastro_prestador.html', context)


def auth_aguardando_aprovacao_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/auth/aguardando_aprovacao.html')