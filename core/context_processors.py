from accounts.models import Prestador

def tipo_usuario_simulado(request):
    """
    Para protótipo estático: deduz 'tipo' a partir do path.
    Em futuro backend, substitua por lógica real (request.user).
    """
    path = request.path or ""
    if path.startswith("/prestador"):
        tipo = "prestador"
    elif path.startswith("/administrador"):
        tipo = "admin"
    elif path.startswith("/"):
        tipo = "cliente"
    else:
        tipo = None
    return {"tipo": tipo}

def lista_cidades(request):
    """
    Disponibiliza a lista de cidades com prestadores ativos em todos os templates.
    """
    cidades = Prestador.objects.values_list('cidade_atendimento', flat=True).distinct().order_by('cidade_atendimento')
    return {'cidades_disponiveis': cidades}