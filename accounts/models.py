from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='categoria_fotos/', null=True, blank=True)

    def __str__(self):
        return self.nome


class CustomUser(AbstractUser):
    class TipoUsuario(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        PRESTADOR = 'PRESTADOR', 'Prestador de Serviço'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'

    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.CLIENTE)
    email = models.EmailField(unique=True, verbose_name='Email')
    telefone = models.CharField(max_length=20, blank=True, null=True)   
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Cliente(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_cliente')
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return f"Cliente: {self.usuario.first_name}"


class Prestador(models.Model):
    class StatusPrestador(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADO = 'APROVADO', 'Aprovado'
        REJEITADO = 'REJEITADO', 'Rejeitado'
    
    class TipoDocumento(models.TextChoices):
        CPF = 'CPF', 'CPF (Pessoa Física)'
        CNPJ = 'CNPJ', 'CNPJ (Pessoa Jurídica)'

    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_prestador')
    
    nome_estabelecimento = models.CharField(max_length=200, verbose_name="Nome do Estabelecimento")
    tipo_documento = models.CharField(max_length=4, choices=TipoDocumento.choices, default=TipoDocumento.CPF)
    documento = models.CharField(max_length=18, unique=True, verbose_name='CPF ou CNPJ')
    cidade_atendimento = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=StatusPrestador.choices, default=StatusPrestador.PENDENTE)
    
    categorias = models.ManyToManyField(Categoria, related_name='prestadores')

    def tem_perfil_completo(self):
        tem_foto_perfil = bool(self.usuario.foto_perfil)
        tem_horarios = self.horarios.exists()
        tem_foto_local = self.fotos_local.exists()
        tem_servico = self.servicos.exists()

        return tem_foto_perfil and tem_horarios and tem_foto_local and tem_servico

    def __str__(self):
        nome_completo = self.usuario.get_full_name() 
        if not nome_completo:
            nome_completo = self.usuario.username
        return f"{nome_completo} ({self.nome_estabelecimento})"


class FotoEstabelecimento(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='fotos_local')
    imagem = models.ImageField(upload_to='estabelecimento_fotos/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.prestador.nome_estabelecimento}"


class Servico(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='servicos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_minutos = models.IntegerField(help_text="Duração em minutos")
    categorias = models.ManyToManyField(Categoria, related_name='servicos')
    foto = models.ImageField(upload_to='servicos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.prestador.nome_estabelecimento}"


class Agendamento(models.Model):
    class StatusAgendamento(models.TextChoices):
        AGENDADO = 'AGENDADO', 'Agendado'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'
        CANCELADO = 'CANCELADO', 'Cancelado'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusAgendamento.choices, default=StatusAgendamento.AGENDADO)
    motivo_cancelamento = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.data_hora_inicio and self.servico:
            self.data_hora_fim = self.data_hora_inicio + timedelta(minutes=self.servico.duracao_minutos)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.servico.nome} em {self.data_hora_inicio.strftime('%d/%m %H:%M')}"


class Avaliacao(models.Model):
    NOTA_CHOICES = [(i, str(i)) for i in range(1, 6)] 
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='avaliacao')
    nota = models.IntegerField(choices=NOTA_CHOICES)


class HorarioFuncionamento(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=[
        (0, 'Domingo'),
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
    ])
    aberto_24h = models.BooleanField(default=False)
    fechado = models.BooleanField(default=False)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fim = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.prestador.nome_estabelecimento}"