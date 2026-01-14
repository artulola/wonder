from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import Prestador
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required

@admin_required
def admin_solicitacoes_view(request: HttpRequest) -> HttpResponse:
    pendentes = Prestador.objects.filter(status=Prestador.StatusPrestador.PENDENTE)
    return render(request, 'core/admin/solicitacoes.html', {'pendentes': pendentes})

@admin_required
def admin_detalhes_solicitacoes_view(request: HttpRequest, prestador_id: int) -> HttpResponse:
    prestador = get_object_or_404(Prestador, id=prestador_id)

    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'aprovar':
            prestador.status = Prestador.StatusPrestador.APROVADO
            prestador.save()
            messages.success(request, 'Prestador aprovado com sucesso!')
        elif acao == 'rejeitar':
            prestador.status = Prestador.StatusPrestador.REJEITADO
            prestador.save()
            messages.warning(request, 'Prestador rejeitado.')
        else:
            messages.error(request, 'Ação inválida.')
        return redirect('admin-solicitacoes')

    return render(request, 'core/admin/detalhes_solicitacao.html', {'prestador': prestador})

@admin_required
def admin_categorias_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/admin/categorias.html')