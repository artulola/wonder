from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Cliente, Prestador, Categoria


class ClienteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-campo', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Nome'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Sobrenome'}))
    telefone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Telefone'}))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Confirmar Senha'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está registrado.')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('As senhas não conferem.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.tipo_usuario = CustomUser.TipoUsuario.CLIENTE
        if commit:
            user.save()
        return user

class ClienteEnderecoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('endereco',)
        widgets = {
            'endereco': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Endereço completo'})
        }


class PrestadorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-campo', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Nome'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Sobrenome'}))
    telefone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Telefone'}))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Confirmar Senha'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está registrado.')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('As senhas não conferem.')
        return p2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.tipo_usuario = CustomUser.TipoUsuario.PRESTADOR
        if commit:
            user.save()
        return user

class PrestadorProfileForm(forms.ModelForm):
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Prestador
        fields = ('nome_estabelecimento', 'tipo_documento', 'documento', 'endereco', 'cidade_atendimento', 'categorias')
        widgets = {
            'nome_estabelecimento': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Nome do Estabelecimento'}),
            'tipo_documento': forms.Select(attrs={'class': 'input-campo'}),
            'documento': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'CPF ou CNPJ'}),
            'endereco': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Endereço do Estabelecimento'}),
            'cidade_atendimento': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Cidade de Atendimento'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'})
    )