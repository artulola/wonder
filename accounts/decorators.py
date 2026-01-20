from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def cliente_required(view_func):
    """
    Verifica se o usuário está logado e se o tipo_usuario é 'CLIENTE'.
    Caso contrário, redireciona para o login (ou outra página definida).
    """
    def check_cliente(user):
        return user.is_authenticated and getattr(user, 'tipo_usuario', '') == 'CLIENTE'
    
    return user_passes_test(check_cliente, login_url='login')(view_func)

def prestador_required(view_func):
    """
    Verifica se o usuário está logado e se o tipo_usuario é 'PRESTADOR'.
    """
    def check_prestador(user):
        return user.is_authenticated and getattr(user, 'tipo_usuario', '') == 'PRESTADOR'
    
    return user_passes_test(check_prestador, login_url='login')(view_func)

def admin_required(view_func):
    """
    Verifica se o usuário está logado e se é 'ADMINISTRADOR' ou Superusuário.
    """
    def check_admin(user):
        return user.is_authenticated and (getattr(user, 'tipo_usuario', '') == 'ADMINISTRADOR' or user.is_staff)
    
    return user_passes_test(check_admin, login_url='login')(view_func)