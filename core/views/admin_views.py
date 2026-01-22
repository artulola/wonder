from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import Prestador, Categoria
from django.http import HttpRequest, HttpResponse
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
    # Ordena por nome para a lista ficar organizada
    categorias = Categoria.objects.all().order_by('nome')

    if request.method == 'POST':
        acao = request.POST.get('acao')

        # 1. CRIAR
        if acao == 'criar':
            nome = request.POST.get('nome')
            foto = request.FILES.get('foto')
            
            # Validação simples para não criar categoria sem nome
            if nome:
                Categoria.objects.create(nome=nome, foto=foto)
                messages.success(request, 'Categoria criada com sucesso!')
            else:
                messages.error(request, 'O nome da categoria é obrigatório.')
            
            return redirect('admin-categorias')

        # 2. EDITAR
        elif acao == 'editar':
            categoria_id = request.POST.get('categoria_id')
            categoria = get_object_or_404(Categoria, id=categoria_id)
            
            novo_nome = request.POST.get('nome')
            if novo_nome:
                categoria.nome = novo_nome
                
            if 'foto' in request.FILES:
                categoria.foto = request.FILES['foto']
                
            categoria.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('admin-categorias')

        # 3. EXCLUIR
        elif acao == 'excluir':
            categoria_id = request.POST.get('categoria_id')
            categoria = get_object_or_404(Categoria, id=categoria_id)
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso!')
            return redirect('admin-categorias')

    return render(request, 'core/admin/categorias.html', {
        'categorias': categorias
    })