from django import forms 
from accounts.models import CustomUser, Cliente

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

class ClienteEnderecoUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['endereco']
        widgets = {
            'endereco': forms.TextInput(attrs= {'class': 'modal-input', 'placeholder': 'Endereço completo'})
        }