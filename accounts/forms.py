from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Cliente, Prestador, Categoria


class ClienteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-campo', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Nome'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Sobrenome'}))
    telefone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Telefone', 'data-mask': 'phone'}))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Confirmar Senha'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está registrado.')
        return email

    def clean_first_name(self):
        nome = self.cleaned_data.get('first_name')
        if nome:
            return nome.strip().title()
        return nome

    def clean_last_name(self):
        sobrenome = self.cleaned_data.get('last_name')
        if sobrenome:
            return sobrenome.strip().title()
        return sobrenome

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
    
    def clean_endereco(self):
        endereco = self.cleaned_data.get('endereco')
        if endereco:
            return endereco.strip().title()
        return endereco

class PrestadorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-campo', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Nome'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Sobrenome'}))
    telefone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Telefone', 'data-mask': 'phone'}))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Confirmar Senha'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está registrado.')
        return email

    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().title()

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().title()

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
            'tipo_documento': forms.Select(attrs={'class': 'input-campo input-select', 'id': 'id_tipo_documento'}),
            'documento': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': '000.000.000-00', 'id': 'id_documento'}),
            'endereco': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Rua, Número - Bairro'}),
            'cidade_atendimento': forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Cidade - UF'}),
            'categorias': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-grid'}),
        }

    def clean_nome_estabelecimento(self):
        nome = self.cleaned_data.get('nome_estabelecimento')
        if nome:
            return nome.strip().title()
        return nome

    def clean_cidade_atendimento(self):
        cidade_input = self.cleaned_data.get('cidade_atendimento')
        if cidade_input:
            cidade_limpa = cidade_input.strip()
            
            cidade_existente = Prestador.objects.filter(cidade_atendimento__iexact=cidade_limpa).first()
            
            if cidade_existente:
                return cidade_existente.cidade_atendimento
                
            return cidade_limpa.title()
            
        return cidade_input

    def clean_endereco(self):
        endereco = self.cleaned_data.get('endereco')
        if endereco:
            return endereco.strip().title()
        return endereco

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto_perfil', 'first_name', 'last_name', 'email', 'telefone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'modal-input', 'placeholder': 'Email'}),
            'telefone': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Telefone'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'modal-input'}),
        }
    
    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().title()

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().title()

    def clean_email(self):
        return self.cleaned_data.get('email', '').strip().lower()

class ClienteEnderecoUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['endereco']
        widgets = {
            'endereco': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Endereço completo'})
        }
    
    def clean_endereco(self):
        return self.cleaned_data.get('endereco', '').strip().title()

class PrestadorEstabelecimentoUpdateForm(forms.ModelForm):
    class Meta:
        model = Prestador
        fields = ['nome_estabelecimento', 'endereco', 'cidade_atendimento'] 
        widgets = {
            'nome_estabelecimento': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Nome do Estabelecimento'}),
            'endereco': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Endereço'}),
            'cidade_atendimento': forms.TextInput(attrs={'class': 'modal-input', 'placeholder': 'Cidade'}),
        }

    def clean_nome_estabelecimento(self):
        return self.cleaned_data.get('nome_estabelecimento', '').strip().title()

    def clean_endereco(self):
        return self.cleaned_data.get('endereco', '').strip().title()

    def clean_cidade_atendimento(self):
        cidade_input = self.cleaned_data.get('cidade_atendimento')
        if cidade_input:
            cidade_limpa = cidade_input.strip()
            cidade_existente = Prestador.objects.filter(cidade_atendimento__iexact=cidade_limpa).first()
            
            if cidade_existente:
                return cidade_existente.cidade_atendimento
                
            return cidade_limpa.title()
        return cidade_input

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'input-campo', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input-campo', 'placeholder': 'Senha'})
    )