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